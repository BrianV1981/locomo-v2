# Search Payload Example (RAG 5.2)

This document visualizes exactly what the Gemini agent "sees" when it executes a hybrid search against the LanceDB vector store. 

This example is pulled directly from the live `V2_MARATHON` run.

### The Agent's Tool Call
```bash
python3 aim_core/aim_cli.py search "Sarah LGBTQ support group"
```

### The RAG Payload (What the Agent Reads)
* **Estimated Token Cost:** ~4,285 tokens
* **Character Length:** 17,140 characters

```text
Output: [
  {
    "id": 0,
    "session_id": "conv-26",
    "type": "locomo_conversation",
    "content": "(1:56 pm on 8 May, 2023) <Sarah>: Hey Jess! Good to see you! How have you been?\n\n(1:56 pm on 8 May, 2023) <Jessica>: Hey Sarah! Good to see you! I'm swamped with the kids & work. What's up with you? Anything new?\n\n(1:56 pm on 8 May, 2023) <Sarah>: I went to a LGBTQ support group yesterday and it was so powerful.\n\n(1:56 pm on 8 May, 2023) <Jessica>: Wow, that's cool, Sarah! What happened that was so awesome? Did you hear any inspiring stories?\n\n(1:56 pm on 8 May, 2023) <Sarah>: The transgender stories were so inspiring! I was so happy and thankful for all the support.\n[Image Description]: This image features a vibrant mural on an urban wall with several notable elements:\n\n1. **Mural**: The central focus is a colorful graffiti-style artwork depicting a character with pink hair wearing headphones. The character has various stickers or drawings around them, including one that says \"You're Beautiful\" and another resembling a heart.\n\n2. **Text**:\n   - Above the mural: Multiple signs reading \"ADSTON\".\n   - On the right side of the mural: A sign saying \"CAUTION SITE ENTRANCE 25m AHEAD\".\n   - Below the character's hand, there is text that reads \"TRANS PRIDE\".\n\n3. **Surroundings**:\n   - The wall also has various other signs and stickers.\n   - There are some safety barriers with labels like \"SAFEGORD CLASSIC FR\" visible at the top of the image.\n\n4. **Setting**: This appears to be an urban street setting, possibly near a caf\u00e9 or establishment named \"ANA COFFEE CO.\" as indicated by another sign on the right side.\n\nThe mural is likely part of a public art initiative promoting inclusivity and awareness for transgender pride.",
    "timestamp": "",
    "metadata": "{\"conversation\": \"conv-26\"}",
    "parent_id": 0,
    "score": 0.9942438006401062,
    "filename": "locomo_v2_fine"
  },
  {
    "id": 45,
    "session_id": "conv-26",
    "type": "locomo_conversation",
    "content": "(2:31 pm on 17 July, 2023) <Jessica>: Wow, Sarah! It really conveys unity and strength - such a gorgeous piece! My kids and I just finished another painting like our last one.\n\n(8:56 pm on 20 July, 2023) <Sarah>: Hey Jessica! Just wanted to say hi!\n\n(8:56 pm on 20 July, 2023) <Jessica>: Hey Sarah! Good to talk to you again. What's up? Anything new since last time?\n\n(8:56 pm on 20 July, 2023) <Sarah>: Hey Jess! A lot's happened since we last chatted - I just joined a new LGBTQ activist group last Tues. I'm meeting so many cool people who are as passionate as I am about rights and community support. I'm giving my voice and making a real difference, plus it's fulfilling in so many ways. It's just great, you know?\n\n(8:56 pm on 20 July, 2023) <Jessica>: That's awesome, Sarah! Glad to hear you found a great group where you can have an impact. Bet it feels great to be able to speak your truth and stand up for what's right. Want to tell me a bit more about it?\n\n(8:56 pm on 20 July, 2023) <Sarah>: Thanks, Jessica! It's awesome to have our own platform to be ourselves and support others' rights. Our group, 'The Pride Alliance', is made of all kinds of people investing in positive changes. We have regular meetings, plan events and campaigns, to get together and support each other.\n\n(8:56 pm on 20 July, 2023) <Jessica>: Wow, Sarah, your group sounds awesome! Supporting each other and making good things happen - that's so inspiring! Have you been part of any events or campaigns lately?",
    "timestamp": "",
    "metadata": "{\"conversation\": \"conv-26\"}",
    "parent_id": 0,
    "score": 0.9857354760169983,
    "filename": "locomo_v2_fine"
  },
  {
    "id": 15,
    "session_id": "conv-26",
    "type": "locomo_conversation",
    "content": "(10:37 am on 27 June, 2023) <Sarah>: I'm still figuring out the details, but I'm thinking of working with trans people, helping them accept themselves and supporting their mental health. Last Friday, I went to an LGBTQ+ counseling workshop and it was really enlightening. They talked about different therapeutic methods and how to best work with trans people. Seeing how passionate these pros were about making a safe space for people like me was amazing.\n\n(10:37 am on 27 June, 2023) <Jessica>: Woah, Sarah, it sounds like you're doing some impressive work. It's inspiring to see your dedication to helping others. What motivated you to pursue counseling?\n\n(10:37 am on 27 June, 2023) <Sarah>: Thanks, Jessica. It really mattered. My own journey and the support I got made a huge difference. Now I want to help people go through it too. I saw how counseling and support groups improved my life, so I started caring more about mental health and understanding myself. Now I'm passionate about creating a safe, inviting place for people to grow.\n\n(10:37 am on 27 June, 2023) <Jessica>: Wow, Sarah! You've gained so much from your own experience. Your passion and hard work to help others is awesome. Keep it up, you're making a big impact!\n\n(10:37 am on 27 June, 2023) <Sarah>: Thanks, Jessica! Your kind words mean a lot.\n\n(10:37 am on 27 June, 2023) <Jessica>: Congrats Sarah! Good on you for going after what you really care about.",
    "timestamp": "",
    "metadata": "{\"conversation\": \"conv-26\"}",
    "parent_id": 0,
    "score": 0.9846220016479492,
    "filename": "locomo_v2_fine"
  },
  {
    "id": 43,
    "session_id": "conv-26",
    "type": "locomo_conversation",
    "content": "(2:31 pm on 17 July, 2023) <Sarah>: Seeing my mentee's face light up when they saw the support was the best! Such a special moment.\n\n(2:31 pm on 17 July, 2023) <Jessica>: Wow, Sarah! They must have felt so appreciated. It's awesome to see the difference we can make in each other's lives. Any other exciting LGBTQ advocacy stuff coming up?\n\n(2:31 pm on 17 July, 2023) <Sarah>: Yay! Next month I'm having an LGBTQ art show with my paintings - can't wait!\n\n(2:31 pm on 17 July, 2023) <Jessica>: Wow, Sarah, that sounds awesome! Can't wait to see your art - got any previews?",
    "timestamp": "",
    "metadata": "{\"conversation\": \"conv-26\"}",
    "parent_id": 0,
    "score": 0.9665247797966003,
    "filename": "locomo_v2_fine"
  },
  {
    "id": 24,
    "session_id": "conv-26",
    "type": "locomo_conversation",
    "content": "(4:33 pm on 12 July, 2023) <Sarah>: Hey Jess, great to chat with you again! So much has happened since we last spoke - I went to an LGBTQ conference two days ago and it was really special. I got the chance to meet and connect with people who've gone through similar journeys. It was such a welcoming environment and I felt totally accepted. I'm really thankful for this amazing community - it's shown me how important it is to fight for trans rights and spread awareness.\n\n(4:33 pm on 12 July, 2023) <Jessica>: Wow, Sarah, that sounds awesome! So glad you felt accepted and supported. Events like these are great for reminding us of how strong community can be!\n\n(4:33 pm on 12 July, 2023) <Sarah>: Yeah, it's true! Having people who back you makes such a huge difference. It's great to see how far LGBTQ rights have come, but there's still plenty of progress to be made. I wanna help make a difference.\n\n(4:33 pm on 12 July, 2023) <Jessica>: Wow, Sarah. We've come so far, but there's more to do. Your drive to help is awesome! What's your plan to pitch in?\n\n(4:33 pm on 12 July, 2023) <Sarah>: Thanks, Jess! I'm still looking into counseling and mental health jobs. It's important to me that people have someone to talk to, and I want to help make that happen.\n\n(4:33 pm on 12 July, 2023) <Jessica>: Wow, Sarah! You're so inspiring for wanting to help others with their mental health. What's pushing you to keep going forward with it?",
    "timestamp": "",
    "metadata": "{\"conversation\": \"conv-26\"}",
    "parent_id": 0,
    "score": 0.9591764211654663,
    "filename": "locomo_v2_fine"
  },
  {
    "id": 38,
    "session_id": "conv-26",
    "type": "locomo_conversation",
    "content": "(1:51 pm on 15 July, 2023) <Sarah>: Yes, I did. It was amazing! I felt so accepted and happy, just being around people who accepted and celebrated me. It's definitely a top memory.\n[Image Description]: This image depicts a group of individuals participating in what appears to be a pride parade or LGBTQ+ celebration event. The participants are holding rainbow flags and signs with messages such as \"LOVE IS LOVE\" and \"EQUALITY.\" They are dressed vibrantly with colorful clothing, wigs, and accessories, showcasing their support for the cause.\n\nKey details include:\n- Multiple people wearing bright colors like red, yellow, green, blue, pink, and purple.\n- A person in a rainbow-colored wig and another with multicolored hair.\n- Signs promoting love, equality, and pride are visible among the participants.\n- The setting seems to be outdoors during daylight.\n\nThe overall atmosphere is one of joy, unity, and celebration.\n\n(1:51 pm on 15 July, 2023) <Jessica>: Wow, what an experience! How did it make you feel?\n\n(1:51 pm on 15 July, 2023) <Sarah>: I felt so proud and grateful - the vibes were amazing and it was comforting to know I'm not alone and have a great community around me.\n\n(1:51 pm on 15 July, 2023) <Jessica>: Wow, Sarah! That's huge! How did it feel to be around so much love and acceptance?\n\n(1:51 pm on 15 July, 2023) <Sarah>: It was awesome, Jessica! Being around people who embrace and back me up is beyond words. It really inspired me.",
    "timestamp": "",
    "metadata": "{\"conversation\": \"conv-26\"}",
    "parent_id": 0,
    "score": 0.9445034265518188,
    "filename": "locomo_v2_fine"
  },
  {
    "id": 16,
    "session_id": "conv-26",
    "type": "locomo_conversation",
    "content": "(1:36 pm on 3 July, 2023) <Sarah>: Since we last spoke, some big things have happened. Last week I went to an LGBTQ+ pride parade. Everyone was so happy and it made me feel like I belonged. It showed me how much our community has grown, it was amazing!\n\n(1:36 pm on 3 July, 2023) <Jessica>: Wow, Sarah, sounds like the parade was an awesome experience! It's great to see the love and support for the LGBTQ+ community. Congrats! Has this experience influenced your goals at all?\n\n(1:36 pm on 3 July, 2023) <Sarah>: Thanks, Jess! It really motivated me for sure. Talking to the community made me want to use my story to help others too - I'm still thinking that counseling and mental health is the way to go. I'm super excited to give back.\n\n(1:36 pm on 3 July, 2023) <Jessica>: Wow, Sarah! That's great! I just signed up for a pottery class yesterday. It's like therapy for me, letting me express myself and get creative. Have you found any activities that make you feel the same way?\n[Image Description]: The image shows a hand holding a yellow frisbee with purple accents on a grassy field. The frisbee has some printed text along its edge:\n\n- \"INNOVATIVE\" is written at the top in large letters.\n- Below that, there are smaller texts which include:\n  - \"PROFESSIONAL\"\n  - Some additional small print below it.\n\nThe setting appears to be an outdoor grassy area with greenery around. The person holding the frisbee has a bracelet on their wrist and is wearing a ring.",
    "timestamp": "",
    "metadata": "{\"conversation\": \"conv-26\"}",
    "parent_id": 0,
    "score": 0.8557488918304443,
    "filename": "locomo_v2_fine"
  },
  {
    "id": 23,
    "session_id": "conv-26",
    "type": "locomo_conversation",
    "content": "(8:18 pm on 6 July, 2023) <Jessica>: Wow, Sarah! It's great you have people to support you, that's really awesome!\n\n(8:18 pm on 6 July, 2023) <Sarah>: I'm so lucky to have such a great support system around me. Their love and encouragement has really helped me accept and grow into my true self. They've been instrumental in my transition.\n\n(8:18 pm on 6 July, 2023) <Jessica>: Glad you have support, Sarah! Unconditional love is so important. Here's a pic of my family camping at the beach. We love it, it brings us closer!\n[Image Description]: This image depicts a group of four individuals enjoying a camping trip on a sandy beach at dusk or early evening. Here are the details:\n\n1. **Setting**: The scene is set on a sandy beach with waves visible in the background.\n2. **Time of Day**: It appears to be either late afternoon or early evening, as indicated by the dim lighting and the glow from the campfire.\n\n3. **Objects**:\n   - A large black Jeep SUV is parked behind the group.\n   - In front of the group, there's a fire pit with flames visible, providing light and warmth.\n   - To the left side of the image, there are camping chairs arranged for seating.\n   - There\u2019s an ice chest (cooler) placed on the sand to keep food or drinks cold.\n\n4. **People**:\n   - Four individuals are seated around the campfire.\n     - One person is sitting in a chair holding what appears to be marshmallows, possibly preparing to roast them over the fire.\n     - Another individual is also near the fire pit with something in their hands.\n     - Two more people are seated on camping chairs.\n\n5. **Additional Details**:\n   - The sky has a gradient of colors from blue to orange, suggesting it's either sunset or sunrise.\n   - There\u2019s some sand and tire tracks visible around the campsite, indicating recent vehicle activity.\n\nThis image captures a moment of relaxation and camaraderie among friends during their beach camping adventure.",
    "timestamp": "",
    "metadata": "{\"conversation\": \"conv-26\"}",
    "parent_id": 0,
    "score": 0.7904757857322693,
    "filename": "locomo_v2_fine"
  },
  {
    "id": 6,
    "session_id": "conv-26",
    "type": "locomo_conversation",
    "content": "(1:14 pm on 25 May, 2023) <Jessica>: That's great, Sarah! Loving the inclusivity and support. Anything you're excited for in the adoption process?\n\n(1:14 pm on 25 May, 2023) <Sarah>: I'm thrilled to make a family for kids who need one. It'll be tough as a single parent, but I'm up for the challenge!\n\n(1:14 pm on 25 May, 2023) <Jessica>: You're doing something amazing! Creating a family for those kids is so lovely. You'll be an awesome mom! Good luck!\n\n(1:14 pm on 25 May, 2023) <Sarah>: Thanks, Jessica! Your kind words really mean a lot. I'll do my best to make sure these kids have a safe and loving home.\n\n(1:14 pm on 25 May, 2023) <Jessica>: No doubts, Sarah. You have such a caring heart - they'll get all the love and stability they need! Excited for this new chapter!\n\n(7:55 pm on 9 June, 2023) <Sarah>: Hey Jessica! How's it going? I wanted to tell you about my school event last week. It was awesome! I talked about my transgender journey and encouraged students to get involved in the LGBTQ community. It was great to see their reactions. It made me reflect on how far I've come since I started transitioning three years ago.\n\n(7:55 pm on 9 June, 2023) <Jessica>: Hey Sarah! Great to hear from you. Sounds like your event was amazing! I'm so proud of you for spreading awareness and getting others involved in the LGBTQ community. You've come a long way since your transition - keep on inspiring people with your strength and courage!",
    "timestamp": "",
    "metadata": "{\"conversation\": \"conv-26\"}",
    "parent_id": 0,
    "score": 0.7353291511535645,
    "filename": "locomo_v2_fine"
  },
  {
    "id": 41,
    "session_id": "conv-26",
    "type": "locomo_conversation",
    "content": "(1:51 pm on 15 July, 2023) <Jessica>: Yeah, Sarah, they're some of my fave memories. It brings us together and brings us happiness. Glad you're here to share in it.\n\n(1:51 pm on 15 July, 2023) <Sarah>: Thanks, Jessica! Really glad to have you as a friend to share my journey. You're awesome!\n\n(1:51 pm on 15 July, 2023) <Jessica>: Thanks, Sarah! Appreciate your friendship. It's great to have a supporter!\n\n(1:51 pm on 15 July, 2023) <Sarah>: No worries, Jess! Your friendship means so much to me. Enjoy your day!\n\n(2:31 pm on 17 July, 2023) <Jessica>: Hey Sarah, hope all's good! I had a quiet weekend after we went camping with my fam two weekends ago. It was great to unplug and hang with the kids. What've you been up to? Anything fun over the weekend?\n\n(2:31 pm on 17 July, 2023) <Sarah>: Hey Jessica! That sounds great! Last weekend I joined a mentorship program for LGBTQ youth - it's really rewarding to help the community.\n\n(2:31 pm on 17 July, 2023) <Jessica>: Wow, Sarah! It's great that you're helping out. How's it going? Got any cool experiences you can share?\n\n(2:31 pm on 17 July, 2023) <Sarah>: The mentoring is going great! I've met some amazing young folks and supported them along the way. It's inspiring to see how resilient and strong they are.\n\n(2:31 pm on 17 July, 2023) <Jessica>: Wow, Sarah, that sounds super rewarding! Young people's resilience is amazing. Care to share some stories?",
    "timestamp": "",
    "metadata": "{\"conversation\": \"conv-26\"}",
    "parent_id": 0,
    "score": 0.5565107464790344,
    "filename": "locomo_v2_fine"
  }
]
Process Group PGID: 479112
```

### Analysis of the Payload
Because the A.I.M. ingestion engine uses **Speaker-Boundary Session Chunking (500-1500 chars)** and **Sandwich Context Expansion (N-1, N, N+1)**, the agent is not fed a single isolated sentence. 

Instead, it receives a beautifully formatted, chronologically contiguous "sandwich" of the dialogue. It sees exactly who was speaking, when it happened, the buildup to the statement, and the reaction afterward, completely preserving narrative context without blowing up the context window with 30,000 tokens of useless history.
