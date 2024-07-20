import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from fighters.models import Fighter

def fetch_fighter_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    infobox = soup.find('table', class_='infobox')

    details = {
        'height': 'N/A',
        'reach': 'N/A',
        'division': 'N/A',
        'style': 'N/A',
        'wins': '0',
        'wins_by_knockout': '0',
        'wins_by_submission': '0',
        'wins_by_decision': '0',
        'losses': '0',
        'losses_by_knockout': '0',
        'losses_by_submission': '0',
        'losses_by_decision': '0',
    }

    if infobox:
        rows = infobox.find_all('tr')
        for row in rows:
            header = row.find('th')
            data = row.find('td')
            if header and data:
                key = header.text.strip().lower()
                value = data.text.strip()

                if 'height' in key:
                    details['height'] = value
                elif 'reach' in key:
                    details['reach'] = value
                elif 'division' in key:
                    details['division'] = value
                elif 'style' in key:
                    details['style'] = value
                elif 'wins' in key and 'by knockout' not in key and 'by submission' not in key and 'by decision' not in key:
                    details['wins'] = value
                elif 'knockout' in key and details['wins_by_knockout'] == 'N/A':
                    details['wins_by_knockout'] = value
                elif 'submission' in key and details['wins_by_submission'] == 'N/A':
                    details['wins_by_submission'] = value
                elif 'decision' in key and details['wins_by_decision'] == 'N/A':
                    details['wins_by_decision'] = value
                elif 'losses' in key and 'by knockout' not in key and 'by submission' not in key and 'by decision' not in key:
                    details['losses'] = value
                elif 'knockout' in key and details['wins_by_knockout'] != 'N/A':
                    details['losses_by_knockout'] = value
                elif 'submission' in key and details['wins_by_submission'] != 'N/A':
                    details['losses_by_submission'] = value
                elif 'decision' in key and details['wins_by_decision'] != 'N/A':
                    details['losses_by_decision'] = value

    return details

class Command(BaseCommand):
    help = 'Scrapes and updates fighter data from the Debuted fighters section'

    def handle(self, *args, **kwargs):
        url = 'https://en.wikipedia.org/wiki/List_of_current_UFC_fighters'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

         # Find the "Debuted fighters" section
        debuted_section = soup.find('h2', {'id': 'Debuted_fighters'}).parent
        current_element = debuted_section.find_next_sibling()

        fighters = []
        def safe_int(value):
            try:
                return int(value)
            except (ValueError, TypeError):
                return 0

        while current_element:
            # Check if the current element is the "See also" section
            if 'mw-heading2' in current_element.get('class', []) and current_element.find('h2', {'id': 'See_also'}):
                break

            if current_element.name == 'table' and 'wikitable' in current_element.get('class', []):
                # Extract fighter data from the table
                for row in current_element.find_all('tr')[1:]:  # Skip the header row
                    cols = row.find_all('td')
                    if len(cols) >= 9:  # Ensure there are enough columns
                        name = cols[1].text.split('(c)')[0].strip()
                        age = cols[2].text.strip()
                        height = cols[3].text.strip()

                        # Fetch detailed info from the fighter's link
                        fighter_link = cols[1].find('a', href=True)
                        fighter_details = {}
                        if fighter_link:
                            fighter_details = fetch_fighter_details('https://en.wikipedia.org' + fighter_link['href'])
                        else:
                            continue

                        # Combine the fighter data
                        fighter_data = {
                            'name': name,
                            'age': age,
                            'height': height,
                            'reach': fighter_details.get('reach', 'N/A'),
                            'division': fighter_details.get('division', 'N/A'),
                            'style': fighter_details.get('style', 'N/A'),
                            'wins': safe_int(fighter_details.get('wins', '0')),
                            'wins_by_knockout': safe_int(fighter_details.get('wins_by_knockout', '0')),
                            'wins_by_submission': safe_int(fighter_details.get('wins_by_submission', '0')),
                            'wins_by_decision': safe_int(fighter_details.get('wins_by_decision', '0')),
                            'losses': safe_int(fighter_details.get('losses', '0')),
                            'losses_by_knockout': safe_int(fighter_details.get('losses_by_knockout', '0')),
                            'losses_by_submission': safe_int(fighter_details.get('losses_by_submission', '0')),
                            'losses_by_decision': safe_int(fighter_details.get('losses_by_decision', '0')),
                        }

                        Fighter.objects.update_or_create(
                            name=name,
                            defaults=fighter_data,
                        )

            current_element = current_element.find_next_sibling()

        self.stdout.write(self.style.SUCCESS('Fighter data scraped and updated successfully'))