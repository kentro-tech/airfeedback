# AirFeedback

Simple feedback collection for Air/FastAPI apps.

## Installation

```bash
pip install airfeedback
```

or with uv:

```bash
uv add airfeedback
```

## Usage

See [tests/demo.py](tests/demo.py) for a complete working example.

```python
import air
from airfeedback import AirFeedback

# Define your save callback
async def save_feedback(user_id: int, text: str, route: str | None):
    # Your save logic here (DB, file, API call, etc.)
    pass

# Initialize AirFeedback
feedback = AirFeedback(on_save=save_feedback)

app = air.Air()

@app.post("/feedback")
async def submit_feedback(request: air.Request, user: CurrentUser):
    return await feedback._submit_handler(request, user)

# Add to your page
@app.page
def index(request: air.Request):
    return air.layouts.mvpcss(
        feedback.button(),
        feedback.modal(),
        air.H1("My App"),
    )
```

## Styling

AirFeedback is unstyled by default. Apply CSS classes to customize appearance for any CSS framework:

```python
# With DaisyUI
feedback.button(class_="btn btn-ghost btn-sm")
feedback.modal(
    modal_class="modal-box",
    textarea_class="textarea textarea-bordered w-full",
    submit_class="btn btn-primary",
)

# With custom CSS
feedback.button(class_="my-custom-button")
feedback.modal(
    textarea_class="my-textarea", 
    submit_class="my-submit-btn"
)
```

## Configuration

AirFeedback accepts the following parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `on_save` | `Callable[[int, str, str\|None], Any]` | Required | Async callback to save feedback. Receives `user_id`, `text`, and `route` |
| `route_path` | `str` | `/feedback` | URL path for feedback submission |
| `button_text` | `str` | `💬 Feedback` | Text displayed on feedback button |
| `success_message` | `str` | `✓ Thanks for your feedback!` | Message shown after successful submission |
| `error_message` | `str` | `Feedback cannot be empty` | Message shown when validation fails |

## Methods

### `button(class_="", **kwargs)`

Returns a feedback button component. The button automatically captures the current route when clicked.

**Parameters:**
- `class_`: CSS classes to apply to the button
- `**kwargs`: Additional HTML attributes

### `modal(modal_class="", form_class="", textarea_class="", submit_class="", cancel_class="", title="Share Your Feedback", title_class="", placeholder="...")`

Returns a feedback modal component.

**Parameters:**
- `modal_class`: CSS classes for modal container
- `form_class`: CSS classes for form element
- `textarea_class`: CSS classes for textarea
- `submit_class`: CSS classes for submit button
- `cancel_class`: CSS classes for cancel button
- `title`: Modal title text (set to `None` to hide)
- `title_class`: CSS classes for title
- `placeholder`: Textarea placeholder text

## Features

- **Database Agnostic**: Uses callback pattern - bring your own storage
- **Framework Agnostic CSS**: Unstyled by default, works with any CSS framework
- **Route Tracking**: Automatically captures the page URL where feedback was submitted
- **User Flexible**: Works with any user object that has an `id` attribute

## License

MIT License - see LICENSE file for details
