# LoCoMo V2 Master Changelog & Correction Documentation

This document exhaustively details every single question and answer that was modified for the LoCoMo V2 release. The corrections are isolated into four distinct categories.

## Category 1: Personal User Corrections (1 Questions)
Tag: `[V2_CORRECTION]`
These are the bespoke, manual corrections applied during forensic live-agent evaluations where the agent successfully outsmarted the original dataset creators (e.g., temporal math corrections and precise entity classifications like 'Summer Sounds').

**Question:** [V2_CORRECTION] When did Melanie read the book "nothing is impossible"?
**Updated Answer:** 2022 (but the book title 'Nothing is Impossible' is fabricated; the transcript only says 'This book I read last year')

## Category 2: The 99 Community Audit Logic Errors (152 Questions)
Tag: `[LOCOMO-AUDIT]`
Sourced strictly from the `dial481/locomo-audit` repository, these 99 questions suffered from 'Ground-Truth Hallucinations' where the human annotators guessed facts not present in the text.

**Question:** [LOCOMO-AUDIT] What fields would Caroline be likely to pursue in her educaton?
**Corrected Answer:** Counseling or mental health

**Question:** [LOCOMO-AUDIT] What is Caroline's identity?
**Corrected Answer:** Transgender woman

**Question:** [LOCOMO-AUDIT] When did Melanie run a charity race?
**Corrected Answer:** The Saturday before 25 May 2023 (approximately May 20, 2023)

**Question:** [LOCOMO-AUDIT] What books has Melanie read?
**Corrected Answer:** Charlotte's Web, an unnamed book about pursuing dreams, and Becoming Nicole

**Question:** [LOCOMO-AUDIT] What LGBTQ+ events has Caroline participated in?
**Corrected Answer:** Pride parade, school speech, support group, LGBTQ conference, mentorship program, activist group

**Question:** [LOCOMO-AUDIT] What did Melanie paint recently?
**Corrected Answer:** sunset

**Question:** [LOCOMO-AUDIT] What activities has Melanie done with her family?
**Corrected Answer:** Pottery, painting, camping, museum, swimming, hiking

**Question:** [LOCOMO-AUDIT] What kind of art does Caroline make?
**Corrected Answer:** Paintings including portraits, figurative works, nature scenes, and stained glass; she has recently experimented with abstract art

**Question:** [LOCOMO-AUDIT] What types of pottery have Melanie and her kids made?
**Corrected Answer:** bowls, cup, pots

**Question:** [LOCOMO-AUDIT] What does Melanie do with her family on hikes?
**Corrected Answer:** On hikes, Melanie's family explores nature, enjoys mountain views, and explores forests (D4:8, D8:34). The marshmallow roasting and storytelling happen around the campfire during camping trips, not on hikes.

**Question:** [LOCOMO-AUDIT] What transgender-specific events has Caroline attended?
**Corrected Answer:** Poetry reading, conference

**Question:** [LOCOMO-AUDIT] When did Melanie's friend adopt a child?
**Corrected Answer:** 2022

**Question:** [LOCOMO-AUDIT] Would Melanie go on another roadtrip soon?
**Corrected Answer:** Uncertain; although the trip started badly with the accident, the family continued and enjoyed the Grand Canyon, suggesting Melanie values family trips

**Question:** [LOCOMO-AUDIT] What are the new shoes that Melanie got used for?
**Corrected Answer:** Running

**Question:** [LOCOMO-AUDIT] What is Melanie's reason for getting into running?
**Corrected Answer:** To de-stress and clear her mind

**Question:** [LOCOMO-AUDIT] What creative project do Mel and her kids do together besides pottery?
**Corrected Answer:** painting

**Question:** [LOCOMO-AUDIT] How long has Melanie been creating art?
**Corrected Answer:** 7 years

**Question:** [LOCOMO-AUDIT] What setback did Melanie face in October 2023?
**Corrected Answer:** The setback (getting hurt, taking a break from pottery) occurred in September 2023, not October. Melanie reported it on October 13, 2023.

**Question:** [LOCOMO-AUDIT] What painting did Melanie show to Caroline on October 13, 2023?
**Corrected Answer:** Two paintings: (1) a sunset-inspired painting with a pink sky (D17:12), and (2) an abstract painting with a blue background (D17:14).

**Question:** [LOCOMO-AUDIT] What kind of painting did Caroline share with Melanie on October 13, 2023?
**Corrected Answer:** A drawing of a woman in a dress (D17:21), a poster (D17:17), and a 'Trans Lives Matter' sign (D17:19)

**Question:** [LOCOMO-AUDIT] What was the poetry reading that Caroline attended about?
**Corrected Answer:** It was a transgender poetry reading where transgender people shared their stories.

**Question:** [LOCOMO-AUDIT] How did Melanie's son handle the accident?
**Corrected Answer:** The son was in the accident and is OK (D18:1, D18:3); the evidence does not describe the son's emotional reaction directly

**Question:** [LOCOMO-AUDIT] What do Melanie's family give her?
**Corrected Answer:** Strength (to keep going)

**Question:** [LOCOMO-AUDIT] Which events has Jon participated in to promote his business venture?
**Corrected Answer:** fair, networking events, dance competition

**Question:** [LOCOMO-AUDIT] How long did it take for Jon to open his studio?
**Corrected Answer:** five months

**Question:** [LOCOMO-AUDIT] What do the dancers in the photo represent?
**Corrected Answer:** They are performing at the festival

**Question:** [LOCOMO-AUDIT] What does Gina say about the dancers in the photo?
**Corrected Answer:** They look graceful

**Question:** [LOCOMO-AUDIT] What did Gina find for her clothing store on 1 February, 2023?
**Corrected Answer:** A wholesaler agreed to supply her store (per Gina's own words in D3:2), though Jon interpreted the news as finding 'the perfect spot' (D3:3)

**Question:** [LOCOMO-AUDIT] What advice does Gina give to Jon about running a successful business?
**Corrected Answer:** This advice ('build relationships with customers, create a strong brand image, stay positive') was given by JON to GINA in D7:5, not by Gina to Jon. The attribution is reversed.

**Question:** [LOCOMO-AUDIT] What kind of professional experience did Gina get accepted for on May 23, 2023?
**Corrected Answer:** fashion internship (but the acceptance was announced on 27 May 2023, not May 23 as stated in the question)

**Question:** [LOCOMO-AUDIT] When did Maria go to the beach?
**Corrected Answer:** December 2022 (answer is correct, citation is wrong)

**Question:** [LOCOMO-AUDIT] When did Maria meet Jean?
**Corrected Answer:** February 24, 2023 (answer is correct, citation is wrong)

**Question:** [LOCOMO-AUDIT] When did John get his degree?
**Corrected Answer:** The week before 2 April 2023 (answer is correct, citation is incomplete)

**Question:** [LOCOMO-AUDIT] What outdoor activities has John done with his colleagues?
**Corrected Answer:** Hiking, mountaineering (answer is correct, citation D16:2 should be D16:1)

**Question:** [LOCOMO-AUDIT] What activities has Maria done with her church friends?
**Corrected Answer:** Hiking, picnic, volunteer work (answer is correct, D28:5 should be D28:8)

**Question:** [LOCOMO-AUDIT] When did John have his first firefighter call-out?
**Corrected Answer:** The Sunday before 31 July 2023 (July 30, 2023)

**Question:** [LOCOMO-AUDIT] What food item did Maria drop off at the homeless shelter?
**Corrected Answer:** Cakes (answer is correct, D25:19 should be D25:20)

**Question:** [LOCOMO-AUDIT] How many weeks passed between Maria adopting Coco and Shadow?
**Corrected Answer:** Approximately 1-2 weeks (7-15 days); one adoption date is hard (~July 28, 2023) but the other is a vague range ("last week" = ~Aug 4-12, 2023), so the exact gap is unresolvable

**Question:** [LOCOMO-AUDIT] What type of workout class did Maria start doing in December 2023?
**Corrected Answer:** aerial yoga (answer is correct, but question says 2023 when it should say 2022)

**Question:** [LOCOMO-AUDIT] What did Maria donate to a homeless shelter in December 2023?
**Corrected Answer:** old car (answer is correct, but question says 2023 when it should say 2022)

**Question:** [LOCOMO-AUDIT] Why did Maria need to help her cousin find a new place to live?
**Corrected Answer:** Her cousin had to leave and find a new place in a hurry (answer is correct, citation should include D21:7)

**Question:** [LOCOMO-AUDIT] What does John think about trying new classes at the yoga studio?
**Corrected Answer:** Trying new stuff is a great way to push yourself and mix things up (from D25:15, John's actual words)

**Question:** [LOCOMO-AUDIT] What pets wouldn't cause any discomfort to Joanna?
**Corrected Answer:** The transcript does not suggest specific pets. Joanna is allergic to reptiles, animals with fur, and cockroaches (D2:23, D5:11). No specific safe pet types are proposed in the conversation.

**Question:** [LOCOMO-AUDIT] What are Joanna's hobbies?
**Corrected Answer:** Writing, reading, watching movies, exploring nature, hiking, cooking and baking, hanging with friends, acting (past passion), DIY/crafts

**Question:** [LOCOMO-AUDIT] When is Nate hosting a gaming party?
**Corrected Answer:** Two weekends after 3 June, 2022 (approximately June 17-18, 2022).

**Question:** [LOCOMO-AUDIT] What book recommendations has Joanna given to Nate?
**Corrected Answer:** 'Eternal Sunshine of the Spotless Mind' movie (D1:16), 'Little Women' movie (D3:17). Joanna also generically recommended finding a fantasy book series (D19:14), but never named a specific title.

**Question:** [LOCOMO-AUDIT] How long did it take for Joanna to finish writing her book?
**Corrected Answer:** Approximately three months (mid-July to late September 2022).

**Question:** [LOCOMO-AUDIT] What is something Nate gave to Joanna that brings her a lot of joy?
**Corrected Answer:** stuffed toy pup (Tilly)

**Question:** [LOCOMO-AUDIT] When did Nate get Tilly for Joanna?
**Corrected Answer:** 25 May, 2022

**Question:** [LOCOMO-AUDIT] How many of Joanna's writing have made it to the big screen?
**Corrected Answer:** Three (as stated by Joanna in D25:4: 'I know this is the third time it's happened').

**Question:** [LOCOMO-AUDIT] When was Joanna's second movie script shown on the big screens?
**Corrected Answer:** The Sunday before 25 October, 2022 (October 23, 2022).

**Question:** [LOCOMO-AUDIT] What is Joanna inspired by?
**Corrected Answer:** Personal experiences, her own journey of self-discovery, Nate, nature, validation, stories about finding courage and taking risks, people she knows, stuff she sees, imagination

**Question:** [LOCOMO-AUDIT] What things has Nate reccomended to Joanna?
**Corrected Answer:** A pet (D2:14), 'The Lord of the Rings' movies (D9:12), a fantasy book series (D9:14), coconut flavoring (D10:11), a book series with battles and characters (D19:17), Xenoblade Chronicles (D27:23), dairy-free margarine or coconut oil (D20:15).

**Question:** [LOCOMO-AUDIT] What mediums does Nate use to play games?
**Corrected Answer:** PC (D27:15-17), Nintendo console (D27:23 - Xenoblade Chronicles). Other platforms cannot be determined from the transcript text alone.

**Question:** [LOCOMO-AUDIT] What alternative career might Nate consider after gaming?
**Corrected Answer:** Cannot be determined from transcript. Nate is passionate about turtles and knows how to care for them, but he never discusses leaving gaming or pursuing animal care professionally.

**Question:** [LOCOMO-AUDIT] What pets does Nate have?
**Corrected Answer:** A dog (Max) and three turtles.

**Question:** [LOCOMO-AUDIT] How many hikes has Joanna been on?
**Corrected Answer:** At least five (D7:6, D8:4, D11:3, D14:19, D28:22)

**Question:** [LOCOMO-AUDIT] How many turtles does Nate have?
**Corrected Answer:** Three

**Question:** [LOCOMO-AUDIT] What state did Joanna visit in summer 2021?
**Corrected Answer:** Indiana (but the visit was in summer 2022, not summer 2021 as the question states).

**Question:** [LOCOMO-AUDIT] What recipes has Joanna made?
**Corrected Answer:** Dairy-free vanilla cake with strawberry filling and coconut cream frosting (D10:11), a delicious treat (D19:8, unnamed), revised old recipe with strawberries and chocolate (D20:2), dairy-free chocolate coconut cupcakes with raspberry frosting (D20:10), chocolate raspberry tart (D21:11), chocolate cake with raspberries (D22:1/D21:13), blueberry coconut milk dessert with gluten-free crust (D21:17).

**Question:** [LOCOMO-AUDIT] What is one of Joanna's favorite movies?
**Corrected Answer:** 'Eternal Sunshine of the Spotless Mind'

**Question:** [LOCOMO-AUDIT] What is Nate's favorite book series about?
**Corrected Answer:** Adventures, magic, and great characters (the specific subject 'dragons' is not stated in the transcript text).

**Question:** [LOCOMO-AUDIT] What does Nate feel he could do when out in cool places like Whispering Falls?
**Corrected Answer:** This is Joanna's statement, not Nate's. Joanna feels she could write a whole movie when out in cool places like Whispering Falls.

**Question:** [LOCOMO-AUDIT] What did Joanna receive from her brother that brought back childhood memories?
**Corrected Answer:** a handwritten letter (from her brother)

**Question:** [LOCOMO-AUDIT] In which month's game did John achieve a career-high score in points?
**Corrected Answer:** July 2023

**Question:** [LOCOMO-AUDIT] Which endorsement deals has John been offered?
**Corrected Answer:** basketball shoes and gear deal with Nike, potential sponsorship with Gatorade, a popular beverage company (unnamed), outdoor gear company

**Question:** [LOCOMO-AUDIT] What sports does John like besides basketball?
**Corrected Answer:** surfing

**Question:** [LOCOMO-AUDIT] After how many weeks did Tim reconnect with the fellow Harry Potter fan from California?
**Corrected Answer:** approximately four weeks

**Question:** [LOCOMO-AUDIT] How many games has John mentioned winning?
**Corrected Answer:** 6

**Question:** [LOCOMO-AUDIT] Which TV series does Tim mention watching?
**Corrected Answer:** That, Wheel of Time

**Question:** [LOCOMO-AUDIT] When did Tim start playing the violin?
**Corrected Answer:** approximately December 2023

**Question:** [LOCOMO-AUDIT] Which career-high performances did John achieve in 2023?
**Corrected Answer:** highest point score, highest assist

**Question:** [LOCOMO-AUDIT] When did John achieve a career-high assist performance?
**Corrected Answer:** December 8, 2023

**Question:** [LOCOMO-AUDIT] What aspects of the Harry Potter universe will be discussed in John's fan project collaborations?
**Corrected Answer:** characters, spells, magical creatures (but this is Tim's fan project, not John's)

**Question:** [LOCOMO-AUDIT] What did John share with the person he skyped about?
**Corrected Answer:** Characters from Harry Potter (but it was Tim who skyped, not John)

**Question:** [LOCOMO-AUDIT] What type of meal does John often cook using a slow cooker?
**Corrected Answer:** The slow cooker meal is unspecified; honey garlic chicken with roasted veg is a separate dish cooked in a pan

**Question:** [LOCOMO-AUDIT] How does Tim stay motivated during difficult study sessions?
**Corrected Answer:** Breaking study into smaller parts: 25 minutes on, then 5 minutes off (Pomodoro technique)

**Question:** [LOCOMO-AUDIT] What did Tim say about his injury on 16 November, 2023?
**Corrected Answer:** Tim did not have an injury. It was John's injury. John (not Tim) said the doctor said it's not too serious.

**Question:** [LOCOMO-AUDIT] What language does Tim know besides German?
**Corrected Answer:** French (Tim took French in high school, per D27:7)

**Question:** [LOCOMO-AUDIT] What book did Tim get in Italy that inspired him to cook?
**Corrected Answer:** John (not Tim) got a cooking book in Italy

**Question:** [LOCOMO-AUDIT] What is John's favorite book series?
**Corrected Answer:** The evidence does not support Harry Potter as John's favorite. John explicitly calls The Hobbit 'one of my favorites' (D20:20).

**Question:** [LOCOMO-AUDIT] What kind of indoor activities has Andrew pursued with his girlfriend?
**Corrected Answer:** boardgames, volunteering at pet shelter, wine tasting

**Question:** [LOCOMO-AUDIT] When did Audrey make muffins for herself?
**Corrected Answer:** Either April 3-9 (Monday-start convention) or April 9-15 (Sunday-start convention), depending on calendar interpretation.

**Question:** [LOCOMO-AUDIT] When did Audrey see a hummingbird?
**Corrected Answer:** last week of April 2023 (approximately April 24-30, 2023)

**Question:** [LOCOMO-AUDIT] Did Andrew have a pet dog during March 2023?
**Corrected Answer:** No

**Question:** [LOCOMO-AUDIT] Where did Audrey get Pixie from?
**Corrected Answer:** Unclear - D2:1 says 'adopted' while D11:4 says 'breeder'. The evidence is contradictory.

**Question:** [LOCOMO-AUDIT] When did Audrey get into an accident in the park?
**Corrected Answer:** approximately between October 16 and 22, 2023

**Question:** [LOCOMO-AUDIT] What are the breeds of Audrey's dogs?
**Corrected Answer:** Contradictory evidence: D19:12 says Jack Russell mixes and Chihuahua mixes; D26:13 says Lab mixes (Pepper, Panda) and Chihuahua mixes (Precious, Pixie)

**Question:** [LOCOMO-AUDIT] What items has Audrey bought or made for her dogs?
**Corrected Answer:** dog tags, toys, dog beds, collars

**Question:** [LOCOMO-AUDIT] When did Andrew adopt Scout?
**Corrected Answer:** a few days before November 22, 2023

**Question:** [LOCOMO-AUDIT] What organization does Audrey donate a portion of his profits to?
**Corrected Answer:** Animal shelter

**Question:** [LOCOMO-AUDIT] Which places or events have John and James planned to meet at?
**Corrected Answer:** VR gaming, McGee's, baseball game

**Question:** [LOCOMO-AUDIT] How was John feeling on April 10, 2022?
**Corrected Answer:** The 'seeking solitude' event occurred on April 18, 2022, not April 10. There is no data about John's feelings on April 10.

**Question:** [LOCOMO-AUDIT] What is the board game where you have to find the imposter that John mentions to James?
**Corrected Answer:** Unknown - the game is described but never named. 'Mafia' is one possibility among several social deduction games.

**Question:** [LOCOMO-AUDIT] Was James feeling lonely before meeting Samantha?
**Corrected Answer:** Most likely yes (defensible inference); the cited evidence supports loneliness but not for the reasons stated in the golden answer

**Question:** [LOCOMO-AUDIT] What kind of games has James tried to develop?
**Corrected Answer:** football simulator (D13:8), virtual world inspired by Witcher 3 (D6:2, D27:2, D27:6), strategy game like Civilization (D22:5)

**Question:** [LOCOMO-AUDIT] How many days did James plan to spend on his trip in Canada?
**Corrected Answer:** 9 days (July 11 to July 20)

**Question:** [LOCOMO-AUDIT] When did John spend time with his sister and dogs?
**Corrected Answer:** The question should ask about JAMES, not John. James spent time with his sister and dogs on July 21, 2022.

**Question:** [LOCOMO-AUDIT] What happened to John's job situation in 2022?
**Corrected Answer:** The golden answer is factually correct; only the citation D4:36 is invalid.

**Question:** [LOCOMO-AUDIT] How long did it take for James to complete his Witcher-inspired game?
**Corrected Answer:** six months (correct answer, wrong citation - should cite D6:2 not D6:1)

**Question:** [LOCOMO-AUDIT] What was James' big moment with Samantha in October 2023?
**Corrected Answer:** The golden answer about the event is correct, but it happened in October 2022, not October 2023 as stated in the question.

**Question:** [LOCOMO-AUDIT] When did James and his family visit Mark and Josh?
**Corrected Answer:** Between November 4-7, 2022 (exact date indeterminable from transcript)

**Question:** [LOCOMO-AUDIT] What did John organize with his friends on May 8, 2022?
**Corrected Answer:** The CS:GO tournament was organized on May 7, 2022 (not May 8 as stated in the question)

**Question:** [LOCOMO-AUDIT] What did John receive for achieving second place in the tournament?
**Corrected Answer:** money and a trophy (correct answer, but evidence should include D12:8 for the trophy)

**Question:** [LOCOMO-AUDIT] Whose phone number did James receive during the beach outing?
**Corrected Answer:** Samantha (correct answer, but evidence must include D19:16 where the name is stated)

**Question:** [LOCOMO-AUDIT] What is John organizing with his siblings?
**Corrected Answer:** a gaming night (correct answer, but evidence must include D20:15 where 'gaming night' is stated)

**Question:** [LOCOMO-AUDIT] What kind of project was Jolene working on in the beginning of January 2023?
**Corrected Answer:** electrical engineering project

**Question:** [LOCOMO-AUDIT] What card game is Deborah talking about?
**Corrected Answer:** an unnamed card game about cats where you draw cards and can attack opponents (Deborah says she does not remember the name)

**Question:** [LOCOMO-AUDIT] Where did Jolene and her partner spend most of September 2023?
**Corrected Answer:** Phuket

**Question:** [LOCOMO-AUDIT] Which countries has Deborah traveled to?
**Corrected Answer:** Indonesia (Bali), Brazil (Rio de Janeiro)

**Question:** [LOCOMO-AUDIT] What milestone did Jolene achieve recently on 4 February, 2023?
**Corrected Answer:** Design and build a sustainable water purifier for a rural community

**Question:** [LOCOMO-AUDIT] According to Jolene, what does exercise help her to feel?
**Corrected Answer:** This is Deborah's statement, not Jolene's. Deborah said exercise makes her feel connected to her body.

**Question:** [LOCOMO-AUDIT] What did Deb share a photo of, which brought a smile to Jolene's face?
**Corrected Answer:** a yellow coffee cup with a handwritten message

**Question:** [LOCOMO-AUDIT] What did Jolene and Anna discuss while watching the sunset by the sea?
**Corrected Answer:** Deborah and Anna (not Jolene) realized they inspire each other while watching the sunset by the sea.

**Question:** [LOCOMO-AUDIT] What is special about the bench at the park near Deborah's house?
**Corrected Answer:** It holds special memories of conversations with her mom

**Question:** [LOCOMO-AUDIT] What habits does Jolene practice to feel balanced?
**Corrected Answer:** yoga, meditation, walks, and mindfulness

**Question:** [LOCOMO-AUDIT] Why did Jolene have to reschedule their meeting with Deborah on September 8, 2023?
**Corrected Answer:** Deborah (not Jolene) already had plans for that day, causing the reschedule.

**Question:** [LOCOMO-AUDIT] What did Jolene recently play that she described to Deb?
**Corrected Answer:** Deborah (not Jolene) recently played a card game about cats.

**Question:** [LOCOMO-AUDIT] What outdoor activity did Jolene suggest doing together with Deborah?
**Corrected Answer:** Surfing

**Question:** [LOCOMO-AUDIT] Which hobby did Sam take up in May 2023?
**Corrected Answer:** Sam did not take up any hobby in May 2023. He was considering painting but explicitly said 'Not yet'.

**Question:** [LOCOMO-AUDIT] What new hobbies did Sam consider trying?
**Corrected Answer:** Painting, kayaking, hiking, cooking, running

**Question:** [LOCOMO-AUDIT] What kind of healthy food suggestions has Evan given to Sam?
**Corrected Answer:** flavored seltzer water, dark chocolate with high cocoa content, air-popped popcorn and fruit, energy balls

**Question:** [LOCOMO-AUDIT] What significant event happened in Sam's life towards the end of summer 2023?
**Corrected Answer:** This event happened to Evan, not Sam. No comparable significant event for Sam is documented at end of summer 2023 beyond his ongoing health journey.

**Question:** [LOCOMO-AUDIT] What kind of writing does Sam do to relax and cope with his health issues?
**Corrected Answer:** journalling, creative writing

**Question:** [LOCOMO-AUDIT] What is the recurring dream that Sam keeps having?
**Corrected Answer:** he's flying/soaring over skyscrapers

**Question:** [LOCOMO-AUDIT] What kind of foods or recipes has Sam recommended to Evan?
**Corrected Answer:** roasted vegetables, grilled chicken and veggie stir-fry

**Question:** [LOCOMO-AUDIT] What kind of healthy meals did Sam start eating after getting a health scare?
**Corrected Answer:** salad, grilled salmon and vegetables, grilled chicken and veggie stir-fry, fruit bowl

**Question:** [LOCOMO-AUDIT] How often does Sam get health checkups?
**Corrected Answer:** Irregularly, at varying intervals (approximately every 2-3 months in mid-2023, then a longer gap)

**Question:** [LOCOMO-AUDIT] What personal health incidents does Evan face in 2023?
**Corrected Answer:** heart palpitations, twisted knee, knee injury (from basketball)

**Question:** [LOCOMO-AUDIT] When did Evan's son fall off his bike?
**Corrected Answer:** Tuesday before December 17, 2023 (approximately December 12, 2023)

**Question:** [LOCOMO-AUDIT] When did Evan have a drunken night with his friends?
**Corrected Answer:** January 9, 2024

**Question:** [LOCOMO-AUDIT] What dish did Sam make on 18 August, 2023 that turned out flavorful?
**Corrected Answer:** grilled dish with salmon and vegetables (but made on August 14, 2023, not August 18)

**Question:** [LOCOMO-AUDIT] What kind of recipe did Evan request from Sam on 19 August, 2023?
**Corrected Answer:** recipes with more vegetables (but requested on August 15, 2023, not August 19)

**Question:** [LOCOMO-AUDIT] What did Evan start painting years ago due to being inspired by a friend's gift?
**Corrected Answer:** The friend's gift was a forest scene painting, but Evan started painting in general (landscapes, nature scenes), not specifically forest scenes.

**Question:** [LOCOMO-AUDIT] What did Evan share with Sam after their hiking trip?
**Corrected Answer:** Sam (not Evan) shared the photo after Sam's own hiking trip.

**Question:** [LOCOMO-AUDIT] What items did Calvin buy in March 2023?
**Corrected Answer:** mansion in Japan, luxury car

**Question:** [LOCOMO-AUDIT] What mishaps has Calvin run into?
**Corrected Answer:** flooding of his mansion, car accident

**Question:** [LOCOMO-AUDIT] Which places or events has Calvin visited in Tokyo?
**Corrected Answer:** music festival, Ferrari dealership, Shibuya crossing, Shinjuku

**Question:** [LOCOMO-AUDIT] What are Dave's hobbies other than fixing cars?
**Corrected Answer:** take a walk, listen to favorite albums, live concerts, photography (hiking is aspirational, not confirmed as practiced hobby)

**Question:** [LOCOMO-AUDIT] When did Calvin buy his second Ferrari?
**Corrected Answer:** second week of October 2023 (approximately October 8-14)

**Question:** [LOCOMO-AUDIT] Which events in Dave's life inspired him to take up auto engineering?
**Corrected Answer:** attending a car show with Dad, working on an old car in a neighbor's garage when he was young, spent a summer restoring an old car with Dad

**Question:** [LOCOMO-AUDIT] What gifts has Calvin received from his artist friends?
**Corrected Answer:** gold necklace with a diamond pendant, custom-made guitar with an octopus on it

**Question:** [LOCOMO-AUDIT] How long was the car modification workshop in San Francisco?
**Corrected Answer:** Approximately 18 days

**Question:** [LOCOMO-AUDIT] What style of guitars does Calvin own?
**Corrected Answer:** custom-made guitar with an octopus on it, shiny purple guitar

**Question:** [LOCOMO-AUDIT] When did Dave buy a vintage camera?
**Corrected Answer:** November 2023

**Question:** [LOCOMO-AUDIT] Which band was Dave's favorite at the music festival in April 2023?
**Corrected Answer:** Aerosmith (but the festival was in March 2023, not April)

**Question:** [LOCOMO-AUDIT] What did Calvin and his friends arrange for in the park?
**Corrected Answer:** This was Dave and his friends, not Calvin. Dave arranged regular walks together in the park with his friends.

**Question:** [LOCOMO-AUDIT] What color glow did Calvin customize his guitar with?
**Corrected Answer:** purple

**Question:** [LOCOMO-AUDIT] Which Disney movie did Dave mention as one of his favorites?
**Corrected Answer:** Ratatouille

**Question:** [LOCOMO-AUDIT] When did Calvin first get interested in cars?
**Corrected Answer:** Cannot be determined from transcript; the 'early age' answer is about Dave, not Calvin

**Question:** [LOCOMO-AUDIT] What tools does Calvin use to boost his motivation for music?
**Corrected Answer:** Cannot be reliably determined; the 'writing lyrics and notes' answer is about Dave's motivation, not Calvin's

**Question:** [LOCOMO-AUDIT] What hobby did Calvin take up recently?
**Corrected Answer:** Photography is Dave's new hobby, not Calvin's. Calvin has not mentioned taking up a new hobby in the recent sessions.

## Category 3: Visual Translation Cache Replacements (0 Questions)
Tag: `[V2_REPLACEMENT]`
Approximately 10% of the dataset relied on dead image links (404/402 HTTP errors). These questions have been neutralized by providing robust LLaVA OCR transcriptions.

## Category 4: Community Issue Reports (4 Questions)
Tag: `[LOCOMO-ISSUES]`
These corrections stem from open tickets filed by the community on the upstream `locomo` or `locomo-v2` repositories (e.g., identifying ambiguous phrasing or speaker misattributions in specific dialogue turns).

**Question:** [LOCOMO-ISSUES] When did Melanie paint a sunrise?
**Corrected Answer:** 2022

**Question:** [LOCOMO-ISSUES] What symbols are important to Caroline?
**Corrected Answer:** Rainbow flag, eagle (symbolizing freedom and pride)

**Question:** [LOCOMO-ISSUES] What is Melanie's hand-painted bowl a reminder of?
**Corrected Answer:** art and self-expression (but this is Caroline's bowl, not Melanie's)

**Question:** [LOCOMO-ISSUES] What is Caroline's hand-painted bowl a reminder of?
**Corrected Answer:** 

