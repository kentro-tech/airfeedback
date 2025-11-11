"""Demo application for AirFeedback."""

import air
from airfeedback import AirFeedback


# Mock user for demo
class MockUser:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


# Simple in-memory storage for demo
feedback_storage = []

async def save_feedback(user_id: int, text: str, route: str | None):
    """Save feedback to in-memory list.  
    
    In real app, save to any database you use and add any logic you'd like to run on feedback submission."""
    feedback_storage.append(
        {
            "user_id": user_id,
            "text": text,
            "route": route,
        }
    )
    print(f"Feedback saved: {feedback_storage[-1]}")


# Initialize AirFeedback
feedback = AirFeedback(on_save=save_feedback)

# Create Air app
app = air.Air()
app.add_middleware(air.SessionMiddleware, secret_key="demo-secret-key")


@app.post("/feedback")
async def submit_feedback(request: air.Request):
    # For demo, use a mock user
    user = MockUser(id=1, name="Demo User")
    return await feedback._submit_handler(request, user)


@app.page
def index(request: air.Request):
    return air.layouts.mvpcss(
        air.Script(src="https://unpkg.com/htmx.org@2.0.8"),
        air.Div(
            feedback.button(),
        ),
        feedback.modal(),
        air.H1("AirFeedback Demo"),
        air.P("Click the feedback button to test the feedback modal."),
        air.H2("Submitted Feedback:"),
        air.P("Refresh page to see current saved in-memory feedback."),
        air.Ul(
            *[
                air.Li(f"User {fb['user_id']} from route `{fb['route']}`: {fb['text']}")
                for fb in feedback_storage
            ]
        )
        if feedback_storage
        else air.P("No feedback submitted yet."),
        title="AirFeedback Demo",
    )
