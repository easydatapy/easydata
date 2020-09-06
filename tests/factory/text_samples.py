english = [
    (
        "Mr. John and Ms. Sarah are here.    Say <b>hello</b>!!!",
        "Mr. John and Ms. Sarah are here. Say hello!!!",
    ),
    (
        "Mr. John and Ms. Sarah are here<br> say hello!!!",
        "Mr. John and Ms. Sarah are here. Say hello!!!",
    ),
    (
        (
            "Good morning Dr. Adams. The patient is waiting for you in room"
            " number test@mail.com..."
        ),
        (
            "Good morning Dr. Adams. The patient is waiting for you in room"
            " number test@mail.com..."
        ),
    ),
    ("uÌˆnicode. HTML entities &lt;3!", "Ünicode. HTML entities <3!"),
    (
        (
            "Lorem ipsum dolor sit amet... Consectetur adipiscing sed do. "
            "* tempor incididunt ut-labore  .   <li>So be <b>it</b>!</li>"
        ),
        (
            "Lorem ipsum dolor sit amet... Consectetur adipiscing sed do. "
            "Tempor incididunt ut-labore. So be it!"
        ),
    ),
]
