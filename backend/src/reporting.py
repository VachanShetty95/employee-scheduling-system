import os
import json
import google.generativeai as genai
from datetime import time


class GeminiAI:
    """
    A class to handle configuration and interactions with Gemini AI.
    """

    @staticmethod
    def initialize():
        """Initialize Gemini AI with the API key."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables. Please set it in your .env file."
            )
        genai.configure(api_key=api_key)


class ReportGenerator:
    """
    A class to generate efficiency reports using Gemini AI.
    """

    @staticmethod
    def generate(employees_needed, employees_attended, factory_output, factory_target):
        """
        Generate an efficiency report.

        Args:
            employees_needed (int): Number of employees needed last week.
            employees_attended (int): Number of employees who attended last week.
            factory_output (float): Output from the factory.
            factory_target (float): Target output for the factory.

        Returns:
            str: Generated report as a string.
        """
        try:
            GeminiAI.initialize()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Gemini AI: {str(e)}")

        try:
            report_model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config={
                    "temperature": 1,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 8192,
                },
            )
            chat_session = report_model.start_chat(history=[])
            Today = time.strftime("%Y%m%d")

            prompt = f"""You are an efficiency manager with extensive experience in creating forecasting reports. Your task is to create an exaggerated and attention-grabbing report based on the provided data. The report should be written in an impressive markdown format, highlighting key variables and providing an assessment of the situation.
        Here are the input variables you will be working with:
        1. Number of employees needed last week: <employees_needed>{employees_needed}</employees_needed>
        2. Number of employees who attended last week: <employees_attended>{employees_attended}</employees_attended>
        3. Output from the factory: <factory_output>{factory_output}</factory_output>
        4. Target Output from the factory:  <Factory_target_output>{factory_target}</factory_target>
        5. Today's date: <today>{Today}</today>
        To create your report, follow these guidelines:
        1. Start with a dramatic title that captures the essence of the report.
        2. Use markdown formatting to make the report visually appealing. Utilize headers, bold text, italics, and bullet points where appropriate.
        3. Highlight the key variables by using bold text or placing them in separate, eye-catching sections.
        4. Exaggerate the importance and impact of the data. Use superlatives, metaphors, and vivid language to make the report more engaging.
        5. Create fictional scenarios or potential consequences based on the data to add drama to the report.
        6. Include a brief analysis of the relationship between the number of employees needed, employees who attended, and factory output.
        7. Provide an over-the-top assessment of the efficiency situation, making bold predictions or recommendations.
        8. Conclude with a call-to-action that emphasizes the urgency of addressing the efficiency issues.
        9. use appropriate emoji where its needed.
        Remember to maintain a professional tone while still injecting excitement and urgency into the report. Your goal is to create a memorable and impactful document that will grab the reader's attention and emphasize the importance of efficiency in the workplace.
        Present your entire report within <report> tags. Use appropriate markdown syntax throughout the report."""

            response = chat_session.send_message(prompt)
            return response.text.strip()
        except Exception as e:
            raise RuntimeError(f"Error generating report: {str(e)}")


class HeadcountPredictor:
    """
    A class to predict headcount requirements using Gemini AI.
    """

    @staticmethod
    def predict(report_content, next_week_target):
        """
        Predict required headcount for next week's target based on the report.

        Args:
            report_content (str): The efficiency report content.
            next_week_target (float): Target production for next week.

        Returns:
            dict: JSON-formatted prediction with headcount requirements.
        """
        try:
            GeminiAI.initialize()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Gemini AI: {str(e)}")

        try:
            prediction_model = genai.GenerativeModel(
                model_name="gemini-exp-1114",
                generation_config={
                    "temperature": 0.1,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 8192,
                },
            )
            chat_session = prediction_model.start_chat(history=[])


            prompt = f"""Analyze this production report and predict headcount needs for next week.
            
                    Previous Report: '{report_content}'
                    Next Week's Target: {next_week_target}

                    Extract the current metrics from the report and calculate the required headcount for next week's target.
                    Provide your response in this exact JSON format:

                    {{
                        "current_analysis": {{
                            "current_output_per_employee": <calculated from report>,
                            "current_attendance_percentage": <calculated from report>,
                            "brief_summary": <1-2 sentence analysis>
                        }},
                        "next_week_prediction": {{
                            "recommended_headcount": <calculated based on target>,
                            "minimum_headcount": <90% of recommended>,
                            "maximum_headcount": <110% of recommended>,
                            "explanation": <1-2 sentence explanation>
                        }},
                        "key_recommendations": [
                            <2 specific action items>
                        ]
                    }}

                    Important:
                    1. Use actual numbers from the report
                    2. Base predictions on the provided next week's target of {next_week_target}
                    3. Return ONLY valid JSON, no additional text"""

            response = chat_session.send_message(prompt)
            return response
        except Exception as e:
            raise RuntimeError(f"Error predicting headcount: {str(e)}")


# Example usage for API Endpoints
def report_generation_api(employees_needed, employees_attended, factory_output, factory_target):
    """
    API endpoint for generating efficiency reports.
    """
    try:
        return ReportGenerator.generate(
            employees_needed, employees_attended, factory_output, factory_target
        )
    except Exception as e:
        return {"error": str(e)}


def predict_headcount_api(report_content, next_week_target):
    """
    API endpoint for predicting headcount requirements.
    """
    try:
        return HeadcountPredictor.predict(report_content, next_week_target)
    except Exception as e:
        return {"error": str(e)}
