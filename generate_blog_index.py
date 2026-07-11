import os
import json
import re
from datetime import datetime

# Define constant paths
POSTS_DIR = os.path.join("assets", "posts")
INDEX_PATH = os.path.join("assets", "blogs.json")

# Lowercase month names for display formatting
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

# Default post contents to migrate if empty
DEFAULT_POSTS = [
    {
        "filename": "working-with-ai.md",
        "content": """---
title: working with ai
date: 2026-03-01
private: false
---
I do think that along with many things that we as humans are clueless about, we need tutorials to actually do things. However, i am also a fan of just figuring things out on my own. But, on that topic, AI does act as another conversational entity other than onesself.

AI is kinda like using a screwdriver and the screwdriver is alive. Thats how i think about it anyways. The screwdriver may have some idea how to use itself or maybe not... it depends. But we still may need to look towards much more experienced people and take inspiration or advice from them."""
    },
    {
        "filename": "birthday.md",
        "content": """---
title: birthday
date: 2026-02-28
private: true
---
for 2 consecutive years, i tried to be happy on this day for it to be my happy birthday, but unfortunately, its not.

Today was my Bachelor's thesis defense.

I was so stressed leading up to this moment. I cried, I sweat, I ached. I did everything and gave all i could. They said that if i did my best, God would do the rest. had i not done enough? What did i fail to do to get robbed of the grade i deserved. What did i do to deserve this. I clearly dont understand.

For context: I woke up with my head filled to the brim with all of these technical thoughts. They haunt me everynight. Its a curse. I wake up and finalize all i could. I print out my script and all i need. I feel like puking, getting sick, stressed out, almost couldnt eat. nevertheless i went.

Despite all that, I knew i was the most prepared. I went to school after a commute ride that lasted longer than any other as i waited and waited as the jeepney arrived to tropical hut. i get off and walked to what felt like a million steps. i rode the train anxiously, got off, and as each step draw closer and closer as i walked down pureza street, i wanted to take two steps back, i took another and i wanted to take 4 back. despite all that i pushed and pushed.

I wanted to present nothing but perfection. I kept wondering if there was something wrong with my method, my work, the product of my blood, sweat, and tears. It would all come to this day where i showed it to people.

As i remembered what catherine's letter said. I am an experience to behold. It rose a fervor spirit in me, so okay, i believed. I went in with all my might ready and with my head held high.

Me and vinze were able to practice. I was honestly proud that he was able to match my pace a bit at the speaking. However, that really easy for him for someone who has everything prepared for them. But *sigh*- i guess i cant blame the stupid....

anyways, we went in to present. Everything was perfect. We finished in time. We presented to the BEST of our ability. Now onto the meat of the things. I was able to answer the questions and defend my study.

However i felt like i hit a hitch with the panelists. For some reason they kept focusing on how someone had to have a misdiagnosis for my thesis to be considered purposeful. I thought the point was to be proactive instead of reactive but okay..

Nevertheless its not really the main focus of the study. I REPEAtEDly steered the narrative skillfully onto the right path. Heck! even the audience who were listening were all bamboozled why this was happening. To them, they were seeing history in the making.

Even the panelists couldnt help but acknowledge the depth of what was infront of them. but they kept focusing on this little stupid superficial thing. I hate it. I fucking hate it.

Now a list of things to describe what happened:

nag sabog ng perlas sa baboy  
kumanta para sa bingi  
Gumawa ng mona lisa para sa bulag  
nag sign language para sa bingi para makausap, pero tinulugan ako  
idk...

am i happy that its done. no. i think im not. I thought even if okay its not the best, it would be fine because its finally done. well no, its finally NOT done because i still have to make a "MAJOR" revision where im supposed to write 3 sentences to add into the background of the study.

I dont know if people still value the right things. They saw how i captured the essence of research at its core. They admitted to it. I dont understand how it happened. I really dont. I did not deserved to be robbed for all the days that i had worked hard to accomplish what i had. And on top off all of it, it happened on my birthday. What a sick joke."""
    },
    {
        "filename": "rants-and-dilemmas-with-ai.md",
        "content": """---
title: rants and dilemmas with AI
date: 2026-01-15
private: true
---
well how do i start. damn. even starting how i write is becoming hard. even words in my head start to twist.

God knows i didnt have this problem at all. I used to be so fucking good at writing. All i couldnt say by words would be able to be expressed in words i dont verbally speak (eg. typing, writing, and most importantly thinking)

okay back to this rant, ramble, yap session. what do i mean that i hate myself for vouching for LLM writing?

well the reason why i hate it is because it made me less creative, dependent, unstructured. things i had no problem with before. My logical reasoning has taken a toll. My sentences often dont make sense. I fear and dread writing letters now because i fear that im not able to express what i want to say, or what i mean.

Just now, typing all of this, Im realizing that nothing is flowing in my brain. Im not feeling that oomph. I swear i really know how im supposed to go with this but ahh. Its the fucking LLMs.

Why the fuck did i use LLMs in the first place? probably(?) mainly (?) because i was lazy. second? when i was NOT lazy anymore, i believed that i didnt have time to do so. because of that, i used llms to do the tedious work of writing what i want to say.

over the course of time, i got too dependent on telling it what i want to say. And this was happening without me actually saying what i want to say. Ive lost the ability to say what i want to say. who knew that was something that could happen.

Now, these LLMs have weird algorithmic tendencies such as hallucinations and assumptions. All of that now introduces more and more problems. currently with my problem that i cant say what i want to say on my own, im also faced with the problem that LLMs cant translate what i want to say without injecting its own false statements and tics.

I hate AI. I was stupid. I also love AI. Machine learning has better applications. but it shouldnt have been for writing.

reading is a bad experience. writing is a bad experience. i hope one day i could regain my love for reading. i hope one day i could also regain my ability to write. one step at a time. but the problem i have is that there isnt enough time for steps. there always isnt enough time.

out of everything in the world, as of 2026, time is what scares me the most."""
    }
]

def format_display_date(dt):
    month = MONTHS[dt.month - 1]
    return f"{month} {dt.year}"

def parse_post(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    metadata = {}
    filename = os.path.basename(file_path)

    # Simple frontmatter parsing
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            for line in frontmatter.strip().split("\n"):
                if ":" in line:
                    key, val = line.split(":", 1)
                    key = key.strip().lower()
                    val = val.strip()
                    # Remove surrounding quotes if present
                    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                        val = val[1:-1]
                    
                    if key == "private":
                        metadata["private"] = val.lower() in ("true", "yes", "1")
                    else:
                        metadata[key] = val

    # Fill in defaults
    if "title" not in metadata:
        name_without_ext = os.path.splitext(filename)[0]
        metadata["title"] = name_without_ext.replace("-", " ").replace("_", " ")

    if "date" not in metadata:
        mtime = os.path.getmtime(file_path)
        dt = datetime.fromtimestamp(mtime)
        metadata["date"] = dt.strftime("%Y-%m-%d")

    if "private" not in metadata:
        metadata["private"] = False

    # Compute display date
    if "display_date" not in metadata:
        date_str = metadata["date"]
        # Try YYYY-MM-DD
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            metadata["display_date"] = format_display_date(dt)
        except ValueError:
            # Try YYYY-MM
            try:
                dt = datetime.strptime(date_str, "%Y-%m")
                metadata["display_date"] = format_display_date(dt)
            except ValueError:
                metadata["display_date"] = date_str  # Use string directly as fallback

    metadata["filename"] = filename
    return metadata

def main():
    # 1. Ensure assets/posts exists
    if not os.path.exists(POSTS_DIR):
        os.makedirs(POSTS_DIR)
        print(f"Created directory: {POSTS_DIR}")

    # 2. Populate defaults if no md/html files exist
    existing_files = [f for f in os.listdir(POSTS_DIR) if f.endswith((".md", ".html"))]
    if not existing_files:
        print("No blog posts found. Migrating default existing blogs...")
        for p in DEFAULT_POSTS:
            p_path = os.path.join(POSTS_DIR, p["filename"])
            with open(p_path, "w", encoding="utf-8") as f:
                f.write(p["content"])
            print(f"Migrated post: {p['filename']}")
        existing_files = [f for f in os.listdir(POSTS_DIR) if f.endswith((".md", ".html"))]

    # 3. Scan and parse files
    posts = []
    for file in existing_files:
        file_path = os.path.join(POSTS_DIR, file)
        try:
            post_data = parse_post(file_path)
            posts.append(post_data)
        except Exception as e:
            print(f"Error parsing {file}: {e}")

    # 4. Sort posts by date descending (newest first)
    # Standard ISO dates string comparisons work fine (e.g. "2026-03-01" > "2026-02-28")
    posts.sort(key=lambda x: x["date"], reverse=True)

    # 5. Output to assets/blogs.json
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    print(f"Successfully generated {INDEX_PATH} with {len(posts)} posts.")

if __name__ == "__main__":
    main()
