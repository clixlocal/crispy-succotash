# crispy-succotash
App which gathers, cleanses and imports post content

## Radian 6 info.

Api docs are found [here](http://socialcloud.radian6.com/docs/read/socialcloud_reference/post_service). To reproduce the data files,
[Get Child Posts](http://socialcloud.radian6.com/docs/read/socialcloud_reference/post_service#h2-get_child_posts_count)
might be the relevant endpoint. [Data Service](http://socialcloud.radian6.com/docs/read/socialcloud_reference/Data_Service)
also looks like it could be relevant.


### Steps to produce CSV report in Radian6:

- Figure out how to get access to preconfigured Topic Profile "Hospital"
- Barnabas Daily (Dashboard Number 2 in the header)
- Run a subset of the hospitals from the topic profile?
- For each of the hospitals open "River of News"
- Then for each one click "Workflow"
- Click the Gear -> Click Export -> CSV -> Hit checkbox for "Include Workflow" -> Export Method: "Direct Download"
- There's a word doc that maps Hospital Name to Hospital ID
- Within Radian 6, when saving the CSV file, actually save by Hospital ID and save file in Master Import Files
- Run the post_processor script
- Capture the number of spam items removed and number of posts added to the master import file
- Runtimes: between 8:15 AM and 8:30 AM and then a second time at 4:30 PM

### Keyword Groups needed for Barnabas Daily report

- BH 08 JCMC
- BH 00 EC 005845
- BH 00 Brand
- BH 01 SBMC
- BH 02 MMC
- BH 03 NBI
- BH 04 CMMC
- BH 05 KMC
- BH 06 CMC
