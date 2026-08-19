class Class:
    name:str = "Unnamed"
    description:str = "This is a DnD5e Class"
    bio:list[str] = [
        "This is a class template",
        "If you see this, this means that this class is unfinished, please report this to the author"
        ]

    requirements:list[dict] = [
        {"type": "strength", "min": 1, "max":30}
    ]


# Specific Classes


class classArtificer(Class):
    name = "Artificer"
    description = "Intelligent people who utilize the powers of alchemy and magical science"
    bio = [
        "Masters of invention, artificers use ingenuity and magic to unlock extraordinary capabilities in objects.",
        "They see magic as a complex system waiting to be decoded and then harnessed in their spells and inventions.",
        "You can find everything you need to play one of these inventors in the next few sections.",
        "",
        "Artificers use a variety of tools to channel their arcane power.",
        "To cast a spell, an artificer might use alchemist's supplies to:",
        "Create a potent elixir,",
        "Calligrapher's supplies to inscribe a sigil of power,",
        "Or tinker's tools to craft a temporary charm.",
        "",
        "The magic of artificers is tied to their tools and their talents,"
        "And few other characters can produce the right tool for a job as well as an artificer."
    ]

    requirements = [{"type":"intelligence","min":13}]









c = classArtificer()

print(c.name)
print(c.description)
print()
print("> " + "\n> ".join(c.bio))
print()
print(f"You must have a(n) {c.requirements[0]["type"].title()} score of {c.requirements[0]["min"]} or higher in order to multiclass in or out of this class.")