# In app.py - This is the complete, correct code.

from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta

app = Flask(__name__)

# In-memory data storage
users = {}
events = {}

# --- Main Route to Serve the Webpage ---
@app.route('/')
def home():
    return render_template('index.html')

# --- User Profile Management ---
@app.route('/register', methods=['POST'])
def register_user():
    """
    FIXED: This now correctly saves office hours and allows user profiles to be updated.
    """
    user_data = request.get_json()
    username = user_data.get('username')

    if not username:
        return jsonify({'error': 'Username is required.'}), 400

    # Save or update the user's profile with all data, including office hours
    users[username] = {
        'height': user_data.get('height'),
        'weight': user_data.get('weight'),
        'job': user_data.get('job'),
        'office_start': user_data.get('office_start'), # Now correctly saved
        'office_end': user_data.get('office_end'),     # Now correctly saved
        'goals': user_data.get('goals', [])
    }
    return jsonify({'message': f'User {username} profile updated successfully.'}), 201

@app.route('/delete_user/<username>', methods=['DELETE'])
def delete_user(username):
    if username in users:
        del users[username]
        if username in events:
            del events[username]
        return jsonify({'message': f'User {username} and all associated data have been deleted.'}), 200
    else:
        return jsonify({'error': 'User not found.'}), 404

# --- Event and Schedule Management ---
@app.route('/schedule_event', methods=['POST'])
def schedule_event():
    event_data = request.get_json()
    username = event_data.get('username')
    
    if not username or username not in users:
        return jsonify({'error': 'Valid username is required.'}), 400

    event_name = event_data.get('event_name')
    start_str = event_data.get('event_start_time')
    end_str = event_data.get('event_end_time')

    if not all([event_name, start_str, end_str]):
        return jsonify({'error': 'Event name, start time, and end time are required.'}), 400

    if username not in events:
        events[username] = []
    
    events[username].append({
        'name': event_name,
        'start_time': datetime.strptime(start_str, '%H:%M'),
        'end_time': datetime.strptime(end_str, '%H:%M')
    })
    
    return jsonify({'message': 'Engagement scheduled successfully.'}), 201

def generate_base_schedule(user_profile):
    """
    NEW: This is the missing function that generates the ideal daily schedule template.
    """
    job_type = user_profile.get('job', 'other')
    office_start_str = user_profile.get('office_start', '09:00')
    office_end_str = user_profile.get('office_end', '17:00')

    if not office_start_str or not office_end_str:
        office_start_str, office_end_str = '09:00', '17:00'

    office_start = datetime.strptime(office_start_str, '%H:%M')
    office_end = datetime.strptime(office_end_str, '%H:%M')
    
    base_schedule = []

    # Morning Routine
    base_schedule.append({'time': '07:00', 'name': 'Wake Up & Hydrate', 'type': 'routine'})
    base_schedule.append({'time': '07:15', 'name': 'Morning Meditation or Stretching (15 mins)', 'type': 'meditation'})
    base_schedule.append({'time': '07:45', 'name': 'Breakfast', 'type': 'meal'})
    
    # Work Block & Hydration
    base_schedule.append({'time': office_start.strftime('%H:%M'), 'name': 'Start Work', 'type': 'work'})
    lunch_time = office_start + timedelta(hours=4)
    base_schedule.append({'time': lunch_time.strftime('%H:%M'), 'name': 'Lunch Break', 'type': 'meal'})

    current_time = office_start
    while current_time < office_end:
        if current_time != office_start:
             base_schedule.append({'time': current_time.strftime('%H:%M'), 'name': 'Drink Water', 'type': 'health'})
        current_time += timedelta(hours=2)

    base_schedule.append({'time': office_end.strftime('%H:%M'), 'name': 'End Work', 'type': 'work'})

    # Evening Routine
    if 'active' in job_type:
        base_schedule.append({'time': (office_end + timedelta(minutes=30)).strftime('%H:%M'), 'name': 'Post-Work Recovery & Stretching', 'type': 'exercise'})
    else:
        base_schedule.append({'time': (office_end + timedelta(minutes=30)).strftime('%H:%M'), 'name': 'Workout / Exercise (45 mins)', 'type': 'exercise'})

    base_schedule.append({'time': '19:00', 'name': 'Dinner', 'type': 'meal'})
    base_schedule.append({'time': '20:00', 'name': 'Family Time / Relaxation', 'type': 'routine'})
    base_schedule.append({'time': '21:30', 'name': 'Wind Down (Read, No Screens)', 'type': 'routine'})
    base_schedule.append({'time': '22:30', 'name': 'Go to Sleep', 'type': 'routine'})

    return base_schedule

@app.route('/get_schedule/<username>', methods=['GET'])
def get_schedule(username):
    if username not in users:
        return jsonify({'error': 'User not found.'}), 404

    user_profile = users.get(username, {})
    user_events = events.get(username, [])
    
    base_schedule = generate_base_schedule(user_profile)
    
    custom_engagements = []
    for event in user_events:
        custom_engagements.append({
            'start_time': event['start_time'],
            'end_time': event['end_time'],
            'name': event['name'],
            'type': 'personal'
        })
    
    final_schedule = []
    for engagement in custom_engagements:
        final_schedule.append({
            'time': f"{engagement['start_time'].strftime('%H:%M')} - {engagement['end_time'].strftime('%H:%M')}",
            'name': engagement['name'],
            'type': engagement['type']
        })

    for item in base_schedule:
        item_time = datetime.strptime(item['time'], '%H:%M')
        is_conflict = False
        for engagement in custom_engagements:
            if engagement['start_time'] <= item_time < engagement['end_time']:
                is_conflict = True
                break
        if not is_conflict:
            final_schedule.append(item)
    
    final_schedule.sort(key=lambda x: datetime.strptime(x['time'].split(' - ')[0], '%H:%M'))
    
    return jsonify({'schedule': final_schedule})

# --- Main Execution ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)