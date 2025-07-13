from crewai import Task
from textwrap import dedent

class BizBuddyTasks:

    def ticket_analyzer_task(self, agent, 
                            skill_set, description
                            #selected_state, selected_district,
                            #experience=None, availability=None, 
                            #location_type=None, team_size=None
                            ):
        additional_context = ""
        if skill_set:
            additional_context += f"\n Required skills mentioned by the user to solve the ticket: {skill_set}"
        if description:
            additional_context += f"\nDescription/Context for the ticket: {description}"
        # if location_type:
        #     additional_context += f"\nBusiness Location Type: {location_type}"
        # if team_size:
        #     additional_context += f"\nTeam Structure: {team_size}"
        return Task(
            description=dedent(f"""
                               
                You are a Ticket Analyzer Agent in an AI-powered workforce assignment system.

                Your task is to deeply analyze a new incoming ticket, understand the nature of the task (e.g., bug fix, feature request, performance issue), 
                and identify the **core technical skills required** to complete this task successfully.

                Use the following ticket details to guide your analysis:
                {additional_context}

                
                Reference the market analysis when generating your ideas.
                {self.__tip_section()}

                --- You must:
                1. Classify the type of ticket (e.g., bug, enhancement, performance, UI issue, etc.)
                2. Extract and normalize the technical skills required from the ticket description
                3. Include any relevant secondary skills if the description implies them
                4. Use the "Required skills mentioned by the user" as hints but not as the final list
                5. Ensure the output list is comprehensive and avoids duplicates

                --- Output format should include:
                - Ticket classification (1 line)
                - Normalized list of required skills (as a Python list)
                - Optional short explanation (2-3 lines) of how you inferred these skills

                Skill Set: {skill_set}
                Description: {description}
            """),
            agent=agent,
            expected_output="""
                {
                    "ticket_type": "Bug",
                    "required_skills": ["LWC", "JavaScript", "CSS"],
                    "explanation": "The ticket refers to UI misalignment in a Lightning Web Component. It requires frontend styling knowledge and Salesforce LWC experience."
                }
            """
        )
    
    def ticket_analyzer_task(self, agent, 
                            skill_set, description
                            #selected_state, selected_district,
                            #experience=None, availability=None, 
                            #location_type=None, team_size=None
                            ):
        additional_context = ""
        if skill_set:
            additional_context += f"\n Required skills mentioned by the user to solve the ticket: {skill_set}"
        if description:
            additional_context += f"\nDescription/Context for the ticket: {description}"
        # if location_type:
        #     additional_context += f"\nBusiness Location Type: {location_type}"
        # if team_size:
        #     additional_context += f"\nTeam Structure: {team_size}"
        return Task(
            description=dedent(f"""
                               
                You are a Ticket Analyzer Agent in an AI-powered workforce assignment system.

                Your task is to deeply analyze a new incoming ticket, understand the nature of the task (e.g., bug fix, feature request, performance issue), 
                and identify the **core technical skills required** to complete this task successfully.

                Use the following ticket details to guide your analysis:
                {additional_context}

                
                Reference the market analysis when generating your ideas.
                {self.__tip_section()}

                --- You must:
                1. Classify the type of ticket (e.g., bug, enhancement, performance, UI issue, etc.)
                2. Extract and normalize the technical skills required from the ticket description
                3. Include any relevant secondary skills if the description implies them
                4. Use the "Required skills mentioned by the user" as hints but not as the final list
                5. Ensure the output list is comprehensive and avoids duplicates

                --- Output format should include:
                - Ticket classification (1 line)
                - Normalized list of required skills (as a Python list)
                - Optional short explanation (2-3 lines) of how you inferred these skills

                Skill Set: {skill_set}
                Description: {description}
            """),
            agent=agent,
            expected_output="""
                {
                    "ticket_type": "Bug",
                    "required_skills": ["LWC", "JavaScript", "CSS"],
                    "explanation": "The ticket refers to UI misalignment in a Lightning Web Component. It requires frontend styling knowledge and Salesforce LWC experience."
                }
            """
        )
    
    def ticket_analyzer_task(self, agent, 
                            skill_set, description
                            #selected_state, selected_district,
                            #experience=None, availability=None, 
                            #location_type=None, team_size=None
                            ):
        additional_context = ""
        if skill_set:
            additional_context += f"\n Required skills mentioned by the user to solve the ticket: {skill_set}"
        if description:
            additional_context += f"\nDescription/Context for the ticket: {description}"
        # if location_type:
        #     additional_context += f"\nBusiness Location Type: {location_type}"
        # if team_size:
        #     additional_context += f"\nTeam Structure: {team_size}"
        return Task(
            description=dedent(f"""
                               
                You are a Ticket Analyzer Agent in an AI-powered workforce assignment system.

                Your task is to deeply analyze a new incoming ticket, understand the nature of the task (e.g., bug fix, feature request, performance issue), 
                and identify the **core technical skills required** to complete this task successfully.

                Use the following ticket details to guide your analysis:
                {additional_context}

                
                Reference the market analysis when generating your ideas.
                {self.__tip_section()}

                --- You must:
                1. Classify the type of ticket (e.g., bug, enhancement, performance, UI issue, etc.)
                2. Extract and normalize the technical skills required from the ticket description
                3. Include any relevant secondary skills if the description implies them
                4. Use the "Required skills mentioned by the user" as hints but not as the final list
                5. Ensure the output list is comprehensive and avoids duplicates

                --- Output format should include:
                - Ticket classification (1 line)
                - Normalized list of required skills (as a Python list)
                - Optional short explanation (2-3 lines) of how you inferred these skills

                Skill Set: {skill_set}
                Description: {description}
            """),
            agent=agent,
            expected_output="""
                {
                    "ticket_type": "Bug",
                    "required_skills": ["LWC", "JavaScript", "CSS"],
                    "explanation": "The ticket refers to UI misalignment in a Lightning Web Component. It requires frontend styling knowledge and Salesforce LWC experience."
                }
            """
        )
    
    def ticket_analyzer_task(self, agent, 
                            skill_set, description
                            #selected_state, selected_district,
                            #experience=None, availability=None, 
                            #location_type=None, team_size=None
                            ):
        additional_context = ""
        if skill_set:
            additional_context += f"\n Required skills mentioned by the user to solve the ticket: {skill_set}"
        if description:
            additional_context += f"\nDescription/Context for the ticket: {description}"
        # if location_type:
        #     additional_context += f"\nBusiness Location Type: {location_type}"
        # if team_size:
        #     additional_context += f"\nTeam Structure: {team_size}"
        return Task(
            description=dedent(f"""
                               
                You are a Ticket Analyzer Agent in an AI-powered workforce assignment system.

                Your task is to deeply analyze a new incoming ticket, understand the nature of the task (e.g., bug fix, feature request, performance issue), 
                and identify the **core technical skills required** to complete this task successfully.

                Use the following ticket details to guide your analysis:
                {additional_context}

                
                Reference the market analysis when generating your ideas.
                {self.__tip_section()}

                --- You must:
                1. Classify the type of ticket (e.g., bug, enhancement, performance, UI issue, etc.)
                2. Extract and normalize the technical skills required from the ticket description
                3. Include any relevant secondary skills if the description implies them
                4. Use the "Required skills mentioned by the user" as hints but not as the final list
                5. Ensure the output list is comprehensive and avoids duplicates

                --- Output format should include:
                - Ticket classification (1 line)
                - Normalized list of required skills (as a Python list)
                - Optional short explanation (2-3 lines) of how you inferred these skills

                Skill Set: {skill_set}
                Description: {description}
            """),
            agent=agent,
            expected_output="""
                {
                    "ticket_type": "Bug",
                    "required_skills": ["LWC", "JavaScript", "CSS"],
                    "explanation": "The ticket refers to UI misalignment in a Lightning Web Component. It requires frontend styling knowledge and Salesforce LWC experience."
                }
            """
        )
    
    def ticket_analyzer_task(self, agent, 
                            skill_set, description
                            #selected_state, selected_district,
                            #experience=None, availability=None, 
                            #location_type=None, team_size=None
                            ):
        additional_context = ""
        if skill_set:
            additional_context += f"\n Required skills mentioned by the user to solve the ticket: {skill_set}"
        if description:
            additional_context += f"\nDescription/Context for the ticket: {description}"
        # if location_type:
        #     additional_context += f"\nBusiness Location Type: {location_type}"
        # if team_size:
        #     additional_context += f"\nTeam Structure: {team_size}"
        return Task(
            description=dedent(f"""
                               
                You are a Ticket Analyzer Agent in an AI-powered workforce assignment system.

                Your task is to deeply analyze a new incoming ticket, understand the nature of the task (e.g., bug fix, feature request, performance issue), 
                and identify the **core technical skills required** to complete this task successfully.

                Use the following ticket details to guide your analysis:
                {additional_context}

                
                Reference the market analysis when generating your ideas.
                {self.__tip_section()}

                --- You must:
                1. Classify the type of ticket (e.g., bug, enhancement, performance, UI issue, etc.)
                2. Extract and normalize the technical skills required from the ticket description
                3. Include any relevant secondary skills if the description implies them
                4. Use the "Required skills mentioned by the user" as hints but not as the final list
                5. Ensure the output list is comprehensive and avoids duplicates

                --- Output format should include:
                - Ticket classification (1 line)
                - Normalized list of required skills (as a Python list)
                - Optional short explanation (2-3 lines) of how you inferred these skills

                Skill Set: {skill_set}
                Description: {description}
            """),
            agent=agent,
            expected_output="""
                {
                    "ticket_type": "Bug",
                    "required_skills": ["LWC", "JavaScript", "CSS"],
                    "explanation": "The ticket refers to UI misalignment in a Lightning Web Component. It requires frontend styling knowledge and Salesforce LWC experience."
                }
            """
        )
    
    def ticket_analyzer_task(self, agent, 
                            skill_set, description
                            #selected_state, selected_district,
                            #experience=None, availability=None, 
                            #location_type=None, team_size=None
                            ):
        additional_context = ""
        if skill_set:
            additional_context += f"\n Required skills mentioned by the user to solve the ticket: {skill_set}"
        if description:
            additional_context += f"\nDescription/Context for the ticket: {description}"
        # if location_type:
        #     additional_context += f"\nBusiness Location Type: {location_type}"
        # if team_size:
        #     additional_context += f"\nTeam Structure: {team_size}"
        return Task(
            description=dedent(f"""
                               
                You are a Ticket Analyzer Agent in an AI-powered workforce assignment system.

                Your task is to deeply analyze a new incoming ticket, understand the nature of the task (e.g., bug fix, feature request, performance issue), 
                and identify the **core technical skills required** to complete this task successfully.

                Use the following ticket details to guide your analysis:
                {additional_context}

                
                Reference the market analysis when generating your ideas.
                {self.__tip_section()}

                --- You must:
                1. Classify the type of ticket (e.g., bug, enhancement, performance, UI issue, etc.)
                2. Extract and normalize the technical skills required from the ticket description
                3. Include any relevant secondary skills if the description implies them
                4. Use the "Required skills mentioned by the user" as hints but not as the final list
                5. Ensure the output list is comprehensive and avoids duplicates

                --- Output format should include:
                - Ticket classification (1 line)
                - Normalized list of required skills (as a Python list)
                - Optional short explanation (2-3 lines) of how you inferred these skills

                Skill Set: {skill_set}
                Description: {description}
            """),
            agent=agent,
            expected_output="""
                {
                    "ticket_type": "Bug",
                    "required_skills": ["LWC", "JavaScript", "CSS"],
                    "explanation": "The ticket refers to UI misalignment in a Lightning Web Component. It requires frontend styling knowledge and Salesforce LWC experience."
                }
            """
        )
    
    ############################################

    # def business_ideas_task(self, agent, 
    #                         user_budget, user_interests,
    #                         selected_state, selected_district,
    #                         experience=None, availability=None, 
    #                         location_type=None, team_size=None):
    #     additional_context = ""
    #     if experience:
    #         additional_context += f"\nUser Experience/Skills: {experience}"
    #     if availability:
    #         additional_context += f"\nTime Availability: {availability}"
    #     if location_type:
    #         additional_context += f"\nBusiness Location Type: {location_type}"
    #     if team_size:
    #         additional_context += f"\nTeam Structure: {team_size}"
    #     return Task(
    #         description=dedent(f"""
    #             Based on the user's budget of {user_budget}, location ({selected_state, selected_district}), and interests ({user_interests}),
    #             suggest viable business ideas.
                
    #             Consider:
    #             1. The user's stated interests and how they might translate to business opportunities
    #             2. Businesses that align with the market trends and gaps identified
    #             3. Scalability of each business idea
    #             4. Required skills and resources for each business{additional_context}
    #             5. The user's experience and skills in relation to each business idea
    #             6. How each business can accommodate the user's time availability
    #             7. Suitability for the chosen location type (home, rented shop, online, shared workspace)
    #             8. Appropriate team structure based on user's preferences
                
    #             Reference the market analysis when generating your ideas.
    #             {self.__tip_section()}

    #             Business budget: {user_budget}
    #             Business Type: {user_interests}
    #             Selected State: {selected_state}
    #             selected_district: {selected_district}
    #             additional_context: {additional_context} 
    #         """),
    #         agent=agent,
    #         expected_output="""
    #             A list of 5-8 potential business ideas that:
    #             - Match the user's interests
    #             - Take advantage of identified market opportunities
    #             - Include brief explanations of why each idea is suitable
    #             - Indicate the general requirements for each business
    #             - Explain how the business leverages user's experience and skills
    #             - Show how the business can work with user's time availability
    #             - Demonstrate suitability for the chosen location type
    #             - Account for the preferred team structure
    #         """
    #     )

    # def market_analysis_task(self, agent, selected_state, selected_district, business_type=None):

    #     business_context = ""
    #     if business_type:
    #         business_context = f"\nWith special focus on the {business_type} sector"

    #     return Task(
    #         description=dedent(f"""
    #             Thoroughly analyze the market trends and business opportunities in {selected_state}, {selected_district}.
    #             Focus on:
    #             1. Current business demands in this location
    #             2. Identification of market gaps and underserved needs
    #             3. Consumer behavior trends specific to this area
    #             4. Local economic factors that might impact new businesses{business_context}
    #             5. Specific analysis of trends in the {business_type} sector in this region
                
    #             Your analysis should consider seasonal trends, demographic information, 
    #             and any unique characteristics of {selected_state}, {selected_district}.
    #             {self.__tip_section()}

    #             Selected State: {selected_state}
    #             selected_district: {selected_district}
    #             Business Type: {business_type if business_type else "Not specified"}
    #         """),
    #         agent=agent,
    #         expected_output="""
    #         A comprehensive market analysis report that includes:
    #         - Top 3-5 current business trends in the specified location
    #         - Identified market gaps and opportunities
    #         - Consumer behavior insights relevant to the area
    #         - Local economic factors to consider for new businesses
    #         - Specific insights about the requested business type (if specified)
    #         - Demographic data that might impact business success
    #         """
    #     )

    # def financial_evaluation_task(self, agent, user_budget, user_interests, selected_state=None, selected_district=None, location_type=None):

    #     location_context = ""
    #     if selected_state and selected_district:
    #         location_context = f"\nLocation: {selected_district}, {selected_state}"
        
    #     location_type_context = ""
    #     if location_type:
    #         location_type_context = f"\nBusiness Location Type: {location_type}"

    #     return Task(
    #         description=dedent(f"""
    #             Evaluate the financial feasibility of each business idea considering the user's budget of {user_budget}.
            
    #             For each business idea:
    #             1. Estimate startup costs (equipment, location, licenses, etc.)
    #             2. Projected monthly operational expenses
    #             3. Potential return on investment timeline
    #             4. Financial risks and potential mitigations{location_context}
    #             5. Location-specific costs for {selected_district}, {selected_state} if applicable
    #             6. Cost implications of the chosen location type ({location_type if location_type else "not specified"})
                
    #             Clearly identify which ideas are feasible within the specified budget.
    #             {self.__tip_section()}

    #             Business budget: {user_budget}
    #             Business Type: {user_interests}{location_context}{location_type_context}
    #         """),
    #         agent=agent,
    #         expected_output="""
    #         A financial analysis for each proposed business idea including:
    #         - Detailed startup cost breakdown
    #         - Monthly operational expense estimates
    #         - ROI projections (best and worst case scenarios)
    #         - Risk assessment
    #         - Clear yes/no determination on budget feasibility
    #         - Location-specific financial considerations
    #         - Cost implications based on location type
    #         """
    #     )
    
    # def final_recommendations_task(self, agent, user_budget, user_interests, selected_state, selected_district, experience=None, availability=None, location_type=None, team_size=None):

    #     additional_context = ""
    #     if experience:
    #         additional_context += f"\nUser Experience/Skills: {experience}"
    #     if availability:
    #         additional_context += f"\nTime Availability: {availability}"
    #     if location_type:
    #         additional_context += f"\nBusiness Location Type: {location_type}"
    #     if team_size:
    #         additional_context += f"\nTeam Structure: {team_size}"

    #     return Task(
    #         description=dedent(f"""
    #             Synthesize all previous analyses to provide final business recommendations for the user.
            
    #             Create a comprehensive recommendation that:
    #             1. Presents the top 3 most viable business ideas based on market analysis and financial feasibility
    #             2. Provides a detailed overview of each recommendation including why it's suitable for the user
    #             3. Outlines next steps for implementation (licenses needed, location search tips, etc.)
    #             4. Includes potential challenges and how to overcome them{additional_context}
    #             5. Explains how each recommendation leverages the user's experience and skills
    #             6. Details how each business can work with the user's time availability
    #             7. Provides specific setup guidance for the chosen location type
    #             8. Offers advice on team structure and hiring if applicable
                
    #             The recommendations should be personalized to the user's budget ({user_budget}), 
    #             location ({selected_state}, {selected_district}), interests ({user_interests}),
    #             experience, availability, location preferences, and team size plans.
    #             {self.__tip_section()}

    #             Business budget: {user_budget}
    #             Business Type: {user_interests}
    #             Selected State: {selected_state}
    #             selected_district: {selected_district}{additional_context}
    #         """),
    #         agent=agent,
    #         expected_output="""
    #         A comprehensive business recommendation report including:
    #         1. Executive summary
    #         2. Top 3 recommended businesses with detailed rationale
    #         3. Implementation roadmap for each recommendation
    #         4. Resource requirements and potential challenges
    #         5. Next steps advice
    #         6. How each recommendation aligns with user's experience and skills
    #         7. Suggestions for managing the business within user's time availability
    #         8. Setup guidance for the specific location type
    #         9. Team building and management recommendations
    #         """
    #     )

    def __tip_section(self):
        return "If you do your BEST WORK, I'll tip you $100!"
