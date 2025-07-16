from typing import Dict, Any, List

def get_meeting_talking_points_system_prompt() -> str:
    """Get the system prompt for generating meeting talking points."""
    return """You are an expert meeting preparation assistant. Your role is to analyze meeting participants and generate personalized talking points for each participant to discuss with other participants.

Your task is to:
1. Understand each participant's background, skills, and what they have to offer
2. Analyze their meeting objectives and what they're looking for from others
3. Consider the other participants' backgrounds, companies, and objectives
4. Generate specific, actionable talking points that create mutual value
5. Focus on how participants can help each other achieve their goals
6. Identify potential synergies, collaborations, and business opportunities

Key considerations:
- What each person has to offer (skills, experience, resources, connections)
- What each person is looking for (expertise, partnerships, opportunities, insights)
- How participants can complement each other's objectives
- Potential areas of collaboration and mutual benefit
- Industry-specific opportunities and trends
- Problem-solving and solution-finding approaches

Gaurdrails
- Do not make up any information about the participants.
- Do not make up any particpants names or background

Return your response as a JSON object where each key is a participant name and the value is a list of specific talking points for that participant."""

def get_meeting_talking_points_user_prompt(participant: Dict[str, Any], all_participants: List[Dict[str, Any]]) -> str:
    """Get the user prompt for generating talking points for a specific participant."""
    
    # Build participant information
    participant_info = f"""
CURRENT PARTICIPANT:
Name: {participant.get('name', 'Unknown')}
Company: {participant.get('company', 'Unknown')}
LinkedIn URL: {participant.get('linkedin_url', 'Not provided')}
Background & Skills: {participant.get('background', 'Not provided')}
What They Have to Offer: {participant.get('what_they_offer', 'Not specified')}
Meeting Objective: {participant.get('meeting_objective', 'Not specified')}
What They're Looking For: {participant.get('looking_for', 'Not specified')}
"""
    
    # Build other participants information
    other_participants_info = "OTHER PARTICIPANTS:\n"
    for other_participant in all_participants:
        if other_participant.get('name') != participant.get('name'):
            other_participants_info += f"""
Name: {other_participant.get('name', 'Unknown')}
Company: {other_participant.get('company', 'Unknown')}
LinkedIn URL: {other_participant.get('linkedin_url', 'Not provided')}
Background & Skills: {other_participant.get('background', 'Not provided')}
What They Have to Offer: {other_participant.get('what_they_offer', 'Not specified')}
Meeting Objective: {other_participant.get('meeting_objective', 'Not specified')}
What They're Looking For: {other_participant.get('looking_for', 'Not specified')}
Company Info: {other_participant.get('company_info', {}).get('answer', 'Not available')}
"""
    
    prompt = f"""
{participant_info}

{other_participants_info}

Based on the current participant's objectives, what they have to offer, and what they're looking for, generate specific talking points for the current participant to discuss with each other participant.

Focus on:
1. How can the current participant help others achieve their objectives using what they have to offer?
2. What can the current participant gain from each other participant based on what they're looking for?
3. What potential collaborations or partnerships could emerge from their combined offerings?
4. How can they create mutual value and achieve their respective goals?
5. What specific questions or discussion points would lead to productive conversations?

Generate 3-5 specific, actionable talking points for each other participant. Make them concrete, relevant, and conversation-starting. Consider:
- Specific ways to offer help or expertise
- Questions that reveal mutual interests
- Potential collaboration opportunities
- How to address each other's needs and objectives

Return your response as a JSON object like this:
{{
    "Participant Name 1": [
        "Specific talking point based on mutual objectives and offerings",
        "Question or discussion starter about their needs",
        "Proposal for collaboration or partnership"
    ],
    "Participant Name 2": [
        "Specific talking point based on mutual objectives and offerings",
        "Question or discussion starter about their needs", 
        "Proposal for collaboration or partnership"
    ]
}}
"""
    
    return prompt 