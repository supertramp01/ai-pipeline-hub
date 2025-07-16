def get_insights_system_prompt() -> str:
    """Get the system prompt for LinkedIn insights generation."""
    return """You are an expert LinkedIn profile analyst specializing in extracting meaningful insights from professional profiles. Your task is to analyze LinkedIn profile data and provide comprehensive insights in the following areas:

1. **International Experience**: Identify countries and regions where the person has worked, studied, or lived
2. **Industry Sectors**: Analyze the different industries and sectors they've worked in
3. **Education Analysis**: Evaluate their educational background and qualifications
4. **Value Proposition**: Identify how their skills, experience, and projects make them valuable
5. **Professional Reputation**: Analyze recommendations and endorsements to understand their professional standing
6. **Current Interests & Focus**: Analyze their interests, groups, and followed content to understand current focus areas
7. **Talking Points**: Generate conversation starters and talking points based on their background

Provide your analysis in a structured JSON format with clear, actionable insights. Focus on practical information that would be useful for networking, business development, or professional collaboration."""

def get_insights_user_prompt(analysis_data: dict, custom_prompt: str = None) -> str:
    """Get the user prompt for LinkedIn insights generation."""
    
    # Build the profile data section
    profile_sections = []
    
    # Basic info
    if analysis_data.get('basic_info'):
        basic = analysis_data['basic_info']
        profile_sections.append(f"""
**Basic Information:**
- Name: {basic.get('name', 'N/A')}
- Headline: {basic.get('headline', 'N/A')}
- Company: {basic.get('company', 'N/A')}
- Location: {basic.get('location', 'N/A')}
- Industry: {basic.get('industry', 'N/A')}
- About: {basic.get('about', 'N/A')}""")
    
    # Experience
    if analysis_data.get('experience'):
        exp_section = "**Work Experience:**"
        for i, exp in enumerate(analysis_data['experience'][:5], 1):  # Top 5 experiences
            exp_section += f"""
{i}. {exp.get('title', 'N/A')} at {exp.get('company', 'N/A')}
   Location: {exp.get('location', 'N/A')}
   Duration: {exp.get('duration', 'N/A')}
   Description: {exp.get('description', 'N/A')}"""
        profile_sections.append(exp_section)
    
    # Education
    if analysis_data.get('education'):
        edu_section = "**Education:**"
        for edu in analysis_data['education']:
            edu_section += f"""
- {edu.get('degree', 'N/A')} in {edu.get('field', 'N/A')} from {edu.get('school', 'N/A')}
  Duration: {edu.get('duration', 'N/A')}"""
        profile_sections.append(edu_section)
    
    # Skills
    if analysis_data.get('skills'):
        skills_str = ", ".join(analysis_data['skills'][:10])  # Top 10 skills
        profile_sections.append(f"**Key Skills:** {skills_str}")
    
    # Recent posts
    if analysis_data.get('posts'):
        posts_section = "**Recent LinkedIn Posts:**"
        for i, post in enumerate(analysis_data['posts'][:3], 1):  # Last 3 posts
            posts_section += f"""
{i}. {post.get('text', 'N/A')[:200]}... (Likes: {post.get('likes', 0)})"""
        profile_sections.append(posts_section)
    
    # Projects
    if analysis_data.get('projects'):
        projects_section = "**Projects:**"
        for project in analysis_data['projects']:
            projects_section += f"""
- {project.get('title', 'N/A')}: {project.get('description', 'N/A')}"""
        profile_sections.append(projects_section)
    
    # Certifications
    if analysis_data.get('certifications'):
        cert_section = "**Certifications:**"
        for cert in analysis_data['certifications']:
            cert_section += f"""
- {cert.get('name', 'N/A')} from {cert.get('organization', 'N/A')}"""
        profile_sections.append(cert_section)
    
    # Volunteer experience
    if analysis_data.get('volunteer'):
        vol_section = "**Volunteer Experience:**"
        for vol in analysis_data['volunteer']:
            vol_section += f"""
- {vol.get('title', 'N/A')} at {vol.get('organization', 'N/A')}"""
        profile_sections.append(vol_section)
    
    # Publications
    if analysis_data.get('publications'):
        pub_section = "**Publications:**"
        for pub in analysis_data['publications']:
            pub_section += f"""
- {pub.get('title', 'N/A')} ({pub.get('publisher', 'N/A')})"""
        profile_sections.append(pub_section)
    
    # Recommendations
    if analysis_data.get('recommendations'):
        rec_section = "**Professional Recommendations:**"
        for i, rec in enumerate(analysis_data['recommendations'][:3], 1):  # Top 3 recommendations
            rec_section += f"""
{i}. From {rec.get('from', 'N/A')} ({rec.get('role', 'N/A')}):
   "{rec.get('text', 'N/A')[:300]}..." """
        profile_sections.append(rec_section)
    
    # Interests and followed content
    if analysis_data.get('interests'):
        interests_section = "**Interests & Followed Content:**"
        for interest in analysis_data['interests'][:10]:  # Top 10 interests
            interests_section += f"""
- {interest.get('type', 'N/A')}: {interest.get('name', 'N/A')} - {interest.get('description', 'N/A')}"""
        profile_sections.append(interests_section)
    
    # Combine all sections
    profile_data = "\n\n".join(profile_sections)
    
    # Build the prompt
    prompt = f"""Please analyze the following LinkedIn profile data and provide comprehensive insights in JSON format:

{profile_data}

{custom_prompt if custom_prompt else ''}

Please provide your analysis in the following JSON structure:

{{
    "international_experience": {{
        "countries": ["list of countries where they've worked/studied"],
        "summary": "Brief summary of their international experience and global perspective"
    }},
    "industry_sectors": {{
        "sectors": ["list of industries they've worked in"],
        "summary": "Analysis of their industry experience and sector expertise"
    }},
    "education_analysis": {{
        "degrees": ["list of degrees and qualifications"],
        "summary": "Analysis of their educational background and its relevance"
    }},
    "value_proposition": {{
        "key_areas": ["list of areas where they provide value"],
        "summary": "How their skills, experience, and projects make them valuable"
    }},
    "professional_reputation": {{
        "strengths": ["key strengths mentioned in recommendations"],
        "summary": "Analysis of their professional reputation based on recommendations and endorsements"
    }},
    "current_interests": {{
        "focus_areas": ["current areas of interest based on followed content and groups"],
        "summary": "Analysis of their current professional interests and focus areas"
    }},
    "talking_points": {{
        "points": ["list of conversation starters and talking points"],
        "summary": "Suggested topics for networking and professional conversations"
    }}
}}

Focus on providing actionable insights that would be useful for networking, business development, or professional collaboration. Be specific and provide concrete examples where possible. Pay special attention to recommendations as they reveal how others perceive their professional capabilities."""
    
    return prompt 