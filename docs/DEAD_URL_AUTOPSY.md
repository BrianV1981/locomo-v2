# LoCoMo V2: Dead URL Autopsy & Final Cut List

This document serves as the historical record for the **87 image URLs** that have been officially cut from the LoCoMo V2 pipeline. 

To prevent cascading dependency failures (re-running OCR models, flattening datasets, etc.), all 87 of these links are officially classified as "DEAD" for the purposes of question triage, but their true technical status is documented below for posterity.

---

## 1. Data URIs (Rebuildable, but Cut)
*Count: 2*

These are not standard URLs, but rather raw base64-encoded image strings embedded directly into the original dataset. While they technically contain the full picture data and can be rendered by a browser, they break standard downloading and verification scripts. We are cutting them for architectural cleanliness.

- `data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD...[truncated]`
- `data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD...[truncated]`

---

## 2. The Dragnet Casualties (Alive, but Slow)
*Count: 11*

These images are technically ALIVE and return valid HTTP 200 responses. However, they are hosted on notoriously slow servers or behind aggressive rate-limiters (e.g., Wikimedia). Because they failed to load fast enough during the initial automated verification dragnet, they were flagged as dead. We are cutting them rather than re-integrating them to save computational overhead.

- https://upload.wikimedia.org/wikipedia/commons/d/de/Ford_Mustang_-_Shuttleworth_Classic_Car_Show_2017_%2833661471822%29.jpg
- https://upload.wikimedia.org/wikipedia/commons/a/a9/Dekkadancers_Mu%C5%BE_z_Malty.jpg
- https://upload.wikimedia.org/wikipedia/commons/d/dd/Tortoises_in_the_Cotswold_Wildlife_Park_restaurant_-_geograph.org.uk_-_1468751.jpg
- https://upload.wikimedia.org/wikipedia/commons/0/0f/Two_on_ramps_%2841411586832%29.jpg
- https://upload.wikimedia.org/wikipedia/commons/8/85/Cliffs_and_mountains_and_sky_at_sunset_--_2_of_33.jpg
- https://upload.wikimedia.org/wikipedia/commons/6/61/2018_DII_Elite_Eight_Northern_State_Signed_Basketball.jpg
- https://upload.wikimedia.org/wikipedia/commons/a/a3/In_a_car_over_a_lake_%28Unsplash%29.jpg
- https://upload.wikimedia.org/wikipedia/commons/4/48/Birdwatching_India_01.jpg
- https://upload.wikimedia.org/wikipedia/en/2/24/Dog_leash.JPG
- https://moderndogmagazine.com/sites/default/files/images/photoentries/photos/pixie%20smiling.jpg
- https://upload.wikimedia.org/wikipedia/commons/6/67/Boston_Skyline_%28193150499%29.jpeg

---

## 3. Legitimate Dead Links (404s, 403s, and Soft 404s)
*Count: 74*

These are the truly dead URLs. They either return hard HTTP errors (404 Not Found, 403 Forbidden), timeout completely, or are "Soft 404s" (e.g., Reddit returning a generic "Image Deleted" placeholder graphic while serving a 200 status code). 

- {'url': 'https://universe.byu.edu/wp-content/uploads/2018/02/IMG_8914.jpg', 'status': 403}
- {'url': 'https://blog.myfitnesspal.com/wp-content/uploads/2019/06/8-Charity-Walking-Events-That-Give-Your-Steps-Extra-Meaning-1200x900.jpg', 'status': 403}
- {'url': 'https://express-images.franklymedia.com/6616/sites/11/2019/05/28094328/IMG_3656.jpg', 'status': 403}
- {'url': 'https://dynaimage.cdn.cnn.com/cnn/digital-images/org/dfc95f14-b325-431c-b977-5b6dc2d35f9c.jpg', 'status': 502}
- {'url': 'https://portlandrescuemission.org/wp-content/uploads/2017/11/20160809_gc_0797-copy.jpg', 'status': 403}
- {'url': 'https://live.staticflickr.com/7284/16241297914_14ea605e4b_b.jpg', 'status': 404}
- {'url': 'https://images.pixexid.com/a-woman-is-joyfully-running-in-a-sunlit-forest-with-four-dogs-of-various-breeds-kn6f7vry.jpeg', 'status': 404}
- {'url': 'https://img-aws.ehowcdn.com/1280x/www.onlyinyourstate.com/wp-content/uploads/2022/12/gym8.jpg', 'status': 530}
- {'url': 'https://tamboracai.com/assets/Megan-Marlow-Acai-Vegan-Cheesecake-Bars_02.jpg', 'status': 404}
- {'url': 'https://s3-us-west-2.amazonaws.com/sportshub2-uploads-prod/files/sites/1567/2018/02/09230004/IMG_8348-e1518217261806.jpg', 'status': 403}
- {'url': 'https://bunundone.com/wp-content/uploads/2019/08/IMG_5619.jpg', 'status': 404}
- {'url': 'https://cdn2.picryl.com/photo/2020/01/16/members-of-the-local-and-us-communities-attend-the-edfa79-1024.jpg', 'status': 403}
- {'url': 'https://mainephysicaltherapy.com/wp-content/uploads/2017/12/Incline-one-arm-cable-pull-down-1.jpg', 'status': 404}
- {'url': 'https://cdn12.picryl.com/photo/2016/12/31/dogs-reward-expect-856f58-1024.jpg', 'status': 403}
- {'url': 'https://alvjewels.com/cdn/shop/products/image_2b791370-8eae-4e4d-8c8f-4fe581f9240a.jpg', 'status': 404}
- {'url': 'https://pixahive.com/wp-content/uploads/2021/02/Virabhadrasana-Warrior-Pose-357219-pixahive.jpg', 'status': 404}
- {'url': 'https://cdn2.picryl.com/photo/2014/07/04/my-public-lands-roadtrip-dalton-highway-in-alaska-19315093341-ddcc96-1024.jpg', 'status': 403}
- {'url': 'https://cdn2.picryl.com/photo/2020/01/13/combat-veterans-associated-with-troops-first-foundation-06145f-1024.jpg', 'status': 403}
- {'url': 'https://necommunitycenter.org/portland/wp-content/uploads/2023/01/Game-in-Progress-with-Ref2-1024x684.jpg', 'status': 404}
- {'url': 'https://musicconservatory.org/wp-content/uploads/2022/12/IMG-2298.png', 'status': 404}
- {'url': 'https://www.news-press.com/gcdn/presto/2018/12/21/PFTM/e043df2d-48d9-4591-a714-f27ecbd42007-GD1.jpg', 'status': 406}
- {'url': 'https://cdn12.picryl.com/photo/2016/12/31/turtle-nature-slow-nature-landscapes-9a70ba-1024.jpg', 'status': 403}
- {'url': 'https://cdn27.picryl.com/photo/1934/01/01/herbert-brutus-ehrmann-papers-1906-1970-sacco-vanzetti-book-review-by-edmund-216c54-1024.jpg', 'status': 403}
- {'url': 'https://live.staticflickr.com/7269/6934706388_7ea340725b_b.jpg', 'status': 404}
- {'url': 'https://sophieelliottfoundation.co.nz/wp-content/uploads/sites/30/2020/08/SLRA-summer-party-james-hopkirk-low-res-026.jpg', 'status': 404}
- {'url': 'https://serafrescaic.com/wp-content/uploads/2018/10/wedding-cake.jpg', 'status': 404}
- {'url': 'https://anomadontheloose.com/wp-content/uploads/2018/01/tam-wua-forest-monastery-cave-walking-meditation-1728368610..jpg', 'status': 404}
- {'url': 'https://upload.wikimedia.org/wikipedia/commons/4/4c/USA_men%27s_national_basketball_team_%2851910110377%29.jpg', 'status': 429}
- {'url': 'https://upload.wikimedia.org/wikipedia/commons/d/d1/Awesomenauts_-_Screenshot_01.jpg', 'status': 429}
- {'url': 'https://content1.getnarrativeapp.com/static/1396e135-13d4-4c37-8183-5d1eaf957c41/Surprise-proposal-picnic-at-cathedral-park-in-Portland-or-.jpg', 'status': 403}
- {'url': 'https://cdn12.picryl.com/photo/2016/12/31/malinois-water-garden-dog-basks-0d19ee-1024.jpg', 'status': 403}
- {'url': 'https://upload.wikimedia.org/wikipedia/commons/3/34/Car_workshop_tools.jpg', 'status': 429}
- {'url': 'https://upload.wikimedia.org/wikipedia/commons/5/50/A_Chihuahua_fetching_a_ball.JPG', 'status': 429}
- {'url': 'https://cdn2.picryl.com/photo/2015/06/09/flowers-bloom-in-a-garden-near-the-memorial-amphitheater-1acba1-1024.jpg', 'status': 403}
- {'url': 'https://cdn12.picryl.com/photo/2016/12/31/water-turtle-on-the-water-animal-animals-a79381-1024.jpg', 'status': 403}
- {'url': 'https://www.naplesnews.com/gcdn/-mm-/06756bca6c979c173ae23c1ba44f60a8fd2bcbee/c\\u003d0-0-3024-4032/local/-/media/2017/04/25/Naples/Naples/636287249454494595-Yoga-4.jpg', 'status': 406}
- {'url': 'https://www.greenbaypressgazette.com/gcdn/presto/2019/07/16/PGRB/fa8d60a1-0a21-421c-b36d-31f4bc2d2b6d-KEW_0720_LC_referendum_Peters_Concrete_pour.png', 'status': 406}
- {'url': 'https://cdn12.picryl.com/photo/2016/12/31/ford-xl-1967-restored-motor-v8-345-hp-transportation-traffic-2d0301-1024.jpg', 'status': 403}
- {'url': 'https://thebaskshop.com/cdn/shop/files/image_8117b42d-0057-492c-9b06-88fc439af683.jpg', 'status': 404}
- {'url': 'https://trendgallery.art/cdn/shop/files/IMG_9647_fa0b4eba-d7f5-48ae-81c9-b471605dd4a9.jpg', 'status': 404}
- {'url': 'https://upload.wikimedia.org/wikipedia/commons/9/91/Old_Geodesy_library_books.jpg', 'status': 429}
- {'url': 'https://www.lifturbanportland.org/uploads/8/3/6/3/83630366/published/warehouse-volunteers.jpg', 'status': 404}
- {'url': 'https://trendgallery.art/cdn/shop/files/IMG_9358_6dd0efff-bb0c-4923-804f-9edc8600fee8.jpg', 'status': 404}
- {'url': 'https://curated-uploads.imgix.net/AgAAAB0AKRRYoR0ZPH-IdLq3DQTvog.jpg', 'status': 402}
- {'url': 'https://cdn11.bigcommerce.com/s-qy9kl0lfci/images/stencil/original/products/62751/75290/Tama_Star_Classic_Tiger_Stripe__70181.1699123066.jpg', 'status': 404}
- {'url': 'https://cdn2.picryl.com/photo/2014/08/13/alejandro-soto-100th-force-support-squadron-auto-hobby-8fa715-1024.jpg', 'status': 403}
- {'url': 'http://thegroundedpractice.com/cdn/shop/products/306F9F91-FDB8-4052-B87B-4692205658E12.jpg', 'status': 404}
- {'url': 'https://www.arup.com/-/media/arup/images/careers-new/early-careers/interns/americas-interns-banner-image.jpg', 'status': 404}
- {'url': 'https://riverstudiodesign.ca/wp-content/uploads/2019/09/overall-office-jpg-1.jpg', 'status': 404}
- {'url': 'https://i2.wp.com/lifecomingalive.com/wp-content/uploads/2018/05/IMG_0960-e1527675276357.jpg', 'status': 400}
- {'url': 'https://pinnaclepooch.com/cdn/shop/products/image_33290672-49cc-42a7-9f1b-fa7bbe93e529.jpg', 'error': 'HTTPSConnectionPool(host=\'pinnaclepooch.com\', port=443): Max retries exceeded with url: /cdn/shop/products/image_33290672-49cc-42a7-9f1b-fa7bbe93e529.jpg (Caused by NameResolutionError("HTTPSConnection(host=\'pinnaclepooch.com\', port=443): Failed to resolve \'pinnaclepooch.com\' ([Errno -2] Name or service not known)"))'}
- {'url': 'https://chensplate.com/wp-content/uploads/2021/02/IMG_8512.jpg', 'error': "HTTPSConnectionPool(host='chensplate.com', port=443): Max retries exceeded with url: /wp-content/uploads/2021/02/IMG_8512.jpg (Caused by SSLError(SSLError(1, '[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:1000)')))"}
- {'url': 'https://www.thriveyogaandwellness.com/wp-content/uploads/2019/06/IMG_6315-e1561295654472.jpg', 'error': 'HTTPSConnectionPool(host=\'www.thriveyogaandwellness.com\', port=443): Max retries exceeded with url: /wp-content/uploads/2019/06/IMG_6315-e1561295654472.jpg (Caused by NameResolutionError("HTTPSConnection(host=\'www.thriveyogaandwellness.com\', port=443): Failed to resolve \'www.thriveyogaandwellness.com\' ([Errno -3] Temporary failure in name resolution)"))'}
- {'url': 'https://www.dawnsilerart.com/wp-content/uploads/sites/3130/2020/11/YCNHTMC-CU9.jpg', 'error': "HTTPSConnectionPool(host='www.dawnsilerart.com', port=443): Max retries exceeded with url: /wp-content/uploads/sites/3130/2020/11/YCNHTMC-CU9.jpg (Caused by ConnectTimeoutError(<HTTPSConnection(host='www.dawnsilerart.com', port=443) at 0x7424c50ffb30>, 'Connection to www.dawnsilerart.com timed out. (connect timeout=25)'))"}
- {'url': 'https://thehammockllc.com/wp-content/uploads/2019/07/Yoga-all-ages.jpg', 'error': 'HTTPSConnectionPool(host=\'thehammockllc.com\', port=443): Max retries exceeded with url: /wp-content/uploads/2019/07/Yoga-all-ages.jpg (Caused by NameResolutionError("HTTPSConnection(host=\'thehammockllc.com\', port=443): Failed to resolve \'thehammockllc.com\' ([Errno -5] No address associated with hostname)"))'}
- {'url': 'https://www.goinbark.com/wp-content/uploads/2016/08/20160820_150554.jpg', 'error': "HTTPSConnectionPool(host='www.goinbark.com', port=443): Max retries exceeded with url: /wp-content/uploads/2016/08/20160820_150554.jpg (Caused by ConnectTimeoutError(<HTTPSConnection(host='www.goinbark.com', port=443) at 0x7424c5130620>, 'Connection to www.goinbark.com timed out. (connect timeout=25)'))"}
- {'url': 'https://community.us.craghoppers.com/wp-content/uploads/2018/05/j3bmicznnmrnfe1uchho.jpg', 'error': "HTTPSConnectionPool(host='community.us.craghoppers.com', port=443): Max retries exceeded with url: /wp-content/uploads/2018/05/j3bmicznnmrnfe1uchho.jpg (Caused by ConnectTimeoutError(<HTTPSConnection(host='community.us.craghoppers.com', port=443) at 0x7424c50fd1f0>, 'Connection to community.us.craghoppers.com timed out. (connect timeout=25)'))"}
- {'url': 'https://exploringtheprime.com/wp-content/uploads/2019/10/IMG_6705-2.jpg', 'error': "HTTPSConnectionPool(host='exploringtheprime.com', port=443): Max retries exceeded with url: /wp-content/uploads/2019/10/IMG_6705-2.jpg (Caused by ConnectTimeoutError(<HTTPSConnection(host='exploringtheprime.com', port=443) at 0x7424c50fd220>, 'Connection to exploringtheprime.com timed out. (connect timeout=25)'))"}
- {'url': 'https://exploringtheprime.com/wp-content/uploads/2019/10/IMG_6849.jpg', 'error': "HTTPSConnectionPool(host='exploringtheprime.com', port=443): Max retries exceeded with url: /wp-content/uploads/2019/10/IMG_6849.jpg (Caused by ConnectTimeoutError(<HTTPSConnection(host='exploringtheprime.com', port=443) at 0x7424c5131520>, 'Connection to exploringtheprime.com timed out. (connect timeout=25)'))"}
- {'url': 'https://www.goodwillfinds.com/on/demandware.static/-/Sites-goodwill-master/default/dw41d27013/images/large/lhyOBm1CPSKy54szJay7vQj/2023/November/14/image_(140).jpg', 'error': 'HTTPSConnectionPool(host=\'www.goodwillfinds.com\', port=443): Max retries exceeded with url: /on/demandware.static/-/Sites-goodwill-master/default/dw41d27013/images/large/lhyOBm1CPSKy54szJay7vQj/2023/November/14/image_(140).jpg (Caused by NameResolutionError("HTTPSConnection(host=\'www.goodwillfinds.com\', port=443): Failed to resolve \'www.goodwillfinds.com\' ([Errno -3] Temporary failure in name resolution)"))'}
- {'url': 'https://www.goodwillfinds.com/on/demandware.static/-/Sites-goodwill-master/default/dwa2341b30/images/large/lhyOBm1CPSKy54szJay7vQj/2023/November/07/image_(170).jpg', 'error': 'HTTPSConnectionPool(host=\'www.goodwillfinds.com\', port=443): Max retries exceeded with url: /on/demandware.static/-/Sites-goodwill-master/default/dwa2341b30/images/large/lhyOBm1CPSKy54szJay7vQj/2023/November/07/image_(170).jpg (Caused by NameResolutionError("HTTPSConnection(host=\'www.goodwillfinds.com\', port=443): Failed to resolve \'www.goodwillfinds.com\' ([Errno -3] Temporary failure in name resolution)"))'}
- https://i.redd.it/jqeodrms8xnb1.jpg
- https://i.redd.it/1jjc5bw9tmgb1.jpg
- https://i.redd.it/s6gfs24m2hpb1.jpg
- https://i.redd.it/a6vjqnq17kcb1.jpg
- https://i.redd.it/usll6z99c2tb1.jpg
- https://i.redd.it/0z7nrwjeqc431.jpg
- https://i.redd.it/al2nryjbov481.jpg
- https://i.redd.it/q46xsv4ciu641.jpg
- https://i.redd.it/g92z4kf3aph91.jpg
- https://i.redd.it/w5v13bfv8r861.jpg
- https://notjustsundaydinner.com/wp-content/uploads/2022/09/peach-cobbler-2.jpg
- https://warpedtable.com/cdn/shop/products/F331B563-AB73-430A-A6DF-3C5E0F91A4D8.jpg
- https://i.redd.it/clg582472ta91.jpg
