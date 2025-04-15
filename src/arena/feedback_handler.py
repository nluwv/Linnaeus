class FeedbackHandler:
    def __init__(self, database):
        self.database = database
        self.current_feedback = None
        self.current_session = {}

    def store_session_data(self, usecase, user_input, model_a_name, model_b_name, 
                          model_a_response, model_b_response):
        self.current_session.update({
            'usecase': usecase,
            'user_input': user_input,
            'model_a_name': model_a_name,
            'model_b_name': model_b_name,
            'model_a_response': model_a_response,
            'model_b_response': model_b_response
        })

    def set_feedback(self, value):
        self.current_feedback = value

    def submit_feedback(self, feedback_motivation):
        if self.current_feedback and self.current_session:
            self.database.log_feedback(
                **self.current_session,
                feedback=self.current_feedback,
                feedback_motivation=feedback_motivation
            )
            return True
        return False