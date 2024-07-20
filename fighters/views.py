from django.shortcuts import render
import json
from openai import OpenAI
from django.http import JsonResponse
from .models import Fighter
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def fighter_list(request):
    fighters = Fighter.objects.all()
    fighter_data = [{
        'id': fighter.id,
        'name': fighter.name,
        'intro': fighter.intro,
        'age': fighter.age,
        'height': fighter.height,
        'reach': fighter.reach,
        'division': fighter.division,
        'style': fighter.style,
        'wins': fighter.wins,
        'wins_by_knockout': fighter.wins_by_knockout,
        'wins_by_submission': fighter.wins_by_submission,
        'wins_by_decision': fighter.wins_by_decision,
        'losses': fighter.losses,
        'losses_by_knockout': fighter.losses_by_knockout,
        'losses_by_submission': fighter.losses_by_submission,
        'losses_by_decision': fighter.losses_by_decision,
    } for fighter in fighters]
    return JsonResponse(fighter_data, safe=False)

def fighter_detail(request, fighter_id):
    try:
        fighter = Fighter.objects.get(pk=fighter_id)
        fighter_data = {
            'name': fighter.name,
            'intro': fighter.intro,
            'age': fighter.age,
            'height': fighter.height,
            'reach': fighter.reach,
            'division': fighter.division,
            'style': fighter.style,
            'wins': fighter.wins,
            'wins_by_knockout': fighter.wins_by_knockout,
            'wins_by_submission': fighter.wins_by_submission,
            'wins_by_decision': fighter.wins_by_decision,
            'losses': fighter.losses,
            'losses_by_knockout': fighter.losses_by_knockout,
            'losses_by_submission': fighter.losses_by_submission,
            'losses_by_decision': fighter.losses_by_decision,
        }
        return JsonResponse(fighter_data)
    except Fighter.DoesNotExist:
        return JsonResponse({'error': 'Fighter not found'}, status=404)
      
@csrf_exempt
def predict_match(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        fighter1_id = data.get('fighter1_id')
        fighter2_id = data.get('fighter2_id')

        try:
            fighter1 = Fighter.objects.get(pk=fighter1_id)
            fighter2 = Fighter.objects.get(pk=fighter2_id)

            prompt = (
                f"Assume there are two UFC fighters with the following stats:\n\n"
                f"Fighter 1:\n"
                f"- Name: {fighter1.name}"
                f"- Intro: {fighter1.intro}"
                f"- Age: {fighter1.age}\n"
                f"- Height: {fighter1.height}\n"
                f"- Reach: {fighter1.reach}\n"
                f"- Division: {fighter1.division}\n"
                f"- Style: {fighter1.style}\n"
                f"- Wins: {fighter1.wins}\n"
                f"- Wins by Knockout: {fighter1.wins_by_knockout}\n"
                f"- Wins by Submission: {fighter1.wins_by_submission}\n"
                f"- Wins by Decision: {fighter1.wins_by_decision}\n"
                f"- Losses: {fighter1.losses}\n"
                f"- Losses by Knockout: {fighter1.losses_by_knockout}\n"
                f"- Losses by Submission: {fighter1.losses_by_submission}\n"
                f"- Losses by Decision: {fighter1.losses_by_decision}\n\n"
                f"Fighter 2:\n"
                f"- Name: {fighter2.name}"
                f"- Intro: {fighter2.intro}"
                f"- Age: {fighter2.age}\n"
                f"- Height: {fighter2.height}\n"
                f"- Reach: {fighter2.reach}\n"
                f"- Division: {fighter2.division}\n"
                f"- Style: {fighter2.style}\n"
                f"- Wins: {fighter2.wins}\n"
                f"- Wins by Knockout: {fighter2.wins_by_knockout}\n"
                f"- Wins by Submission: {fighter2.wins_by_submission}\n"
                f"- Wins by Decision: {fighter2.wins_by_decision}\n"
                f"- Losses: {fighter2.losses}\n"
                f"- Losses by Knockout: {fighter2.losses_by_knockout}\n"
                f"- Losses by Submission: {fighter2.losses_by_submission}\n"
                f"- Losses by Decision: {fighter2.losses_by_decision}\n\n"
                f"Based on these stats, who is more likely to win the match in reality? Please provide your prediction in the following format:\n"
                f"Prediction: [Winner's name]\n"
                f"Reason: [Provide a brief reason for the prediction in one sentence. This field cannot be blank.]\n"
                f"Make sure the reason is informative and relevant to the fighters' stats."
            )

            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert UFC match predictor."},
                    {"role": "user", "content": prompt}
                ]
            )

            prediction_text = completion.choices[0].message.content.strip()
            prediction_lines = prediction_text.split('\n')
            prediction = {
                'prediction': prediction_lines[0].replace("Prediction: ", ""),
                'reason': prediction_lines[1].replace("Reason: ", "") if len(prediction_lines) > 1 else "",
                'prompt': prompt,
            }

            return JsonResponse(prediction)

        except Fighter.DoesNotExist:
            return JsonResponse({'error': 'One or both fighters not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=400)