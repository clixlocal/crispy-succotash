#Script for preparing each day's export of radian posts for import to sf
# Inputs - Each hosptials REVIEWED AND TAGGED radian exports
# Process - Takes files, fixes, builds single import file, archive's numbers
# Output - the day's master import sheet,  an email summary containing the number of posts created, removed due to spam rules and also those posts with sentiment

# Status 1/4
# Stable. Contains spam rules. Identifies and kills spam posts based on rules related to author, headline, content and url. Spam reduction working as good as Matt F's spam reduction work last week. 

# Next Verion Should Include
# - Auto importing to sf via api
# - Improved and possiblly learning spam removal
# - Spam posts archived in csv
# - Add hosptial names to pretty table which will require ids be stored in dictionary rather than list
# - Improved archiving of app activity and user feedback
# - Needs to take into consideration that ont all rivers will have content and therefore not all csv's must exist. If they do not the user should be warned and asked to continue
# - App should maintain a backup of all posts provided to it so we can overcome any isssue of posts get deleted somewhere on accident
# - App should accept user input for adding authors, content keywords and urls to block. therefore should also be able to quarty whats being blocked and what hve you
# - For better reporting of Processed posts and spam counts by hosptial we might consisider storing all in dicitonary or truple
# Bucket List
# - Radian api post gathering and archiving
# - Loading posts into a que for analytist tagging
#- Next version should archive article ids of all posts processed and not processes them twice, this would eliminate the dupe url errors and give us easier tracking of daily numbers



import csv
import time
from datetime import timedelta
from datetime import date
from datetime import tzinfo, timedelta, datetime
from dateutil import parser
from prettytable import PrettyTable
from simple_salesforce import Salesforce



posts_processed = 0
headline_table = PrettyTable()
headline_table.field_names = ['HOSPTIAL ID', 'ARTICLE ID', 'POST TITLE', 'LENGTH']
headline_table.align['POST TITLE'] = "l" # Left align city names
spam_run_count = 0
spam_article_ids = []
spam_posts_count = 0
sfcon = 0
posts_created = 0

    
def archive_spam(h, article_id, pub_date, spam_category, spam_key, spam_content, url):
    global spam_run_count
    global spam_article_ids
    global spam_posts_count
    
    spam_run_count = spam_run_count + 1
       
    if spam_run_count <=  1:
        spam_posts_count = spam_posts_count + 1
        spam_posts_file = open('spamposts.csv', 'wb')
        spam_posts = csv.writer(spam_posts_file, delimiter=',')
        spam_posts.writerow(['Spam Post Count', 'Hospital Id' , 'Post Id', 'Published Date', 'Spam Rule Category', 'Spam Key', 'Spam Content', 'Url'])
        spam_posts.writerow([spam_posts_count, h, article_id, pub_date, spam_category, spam_key, spam_content, url])
    else:
        if not article_id in spam_article_ids:
            spam_article_ids.append(article_id)
            spam_posts_count = spam_posts_count + 1
            spam_posts_file = open('spamposts.csv', 'a')
            spam_posts = csv.writer(spam_posts_file, delimiter=',')
            spam_posts.writerow([spam_posts_count, h, article_id, pub_date, spam_category, spam_key, spam_content, url])
        else:
            return spam_posts_count
            
    spam_posts_file.close()
        
def remove_spam(h, post):
    #notes:
        # all spam numbers should be archived
        # all spam posts should be archived to a csv for reference to make sure all is ok

    flag = 0
    authors_to_exclude = ['Clara Maass Medical Center', 'Jersey City Medical Center', 'Newark Beth Israel', 'Monmouth Medical Center', 'Barnabas Health', 'COMMUNITY MEDICAL CENTER', 'Saint Barnabas Medical Center', 'Chapel', 'CALIFORNIA_COMP', 'London', 'Pittsburgh', 'RZ_RAQUEL', 'FUTURAMIAH', 'Saints_TOPNews', 'BRIANDYP_FS', '_E192', 'MONMOUTH MEDICAL CENTER', 'JERSEY_CITY_JOB', 'JOBSATBARNABAS', 'TMJ_NJ_HEALTH', 'BARNABAS', 'TMJ_NYC_HEALTH', 'TMJ_NYC_NURSING', 'NEWARK BETH', 'JERSEY CITY MEDICAL', 'NEWARK_BETH', 'CLARA', 'BARNHEALTHACC', 'JOB', 'LINCOLNSHIRE']
    headlines_to_exclude = ['TWEET FROM: WPGC', 'Chapel', 'Danesmoor', 'pope', 'Cricket', 'ArabBrains', 'Pittsburgh', 'Soup Kitchen', 'SAINTS_TOPNEWS', 'bronx', '#job']
    content_to_exclude = ['parishioners', 'DCTraffic ', 'Zumba', 'Jericho', 'mdtraffic', 'Sierra Leone','Quarry', 'Bishop', 'pastor', 'I__Barnabas', 'Italy', 'Danesmoor', 'Soup Kitchen', 'on saint Barnabas', 'pope', 'Littlehampton', 'Fordham', 'Perugia', 'chapel', 'Famagusta', 'mission trip', 'High School', 'Barnabas UMC', 'librarian', 'Barnabas Chicago', 'Gereja', 'pupils', 'Barnabas hospice', 'Lincoln', 'new GUINEA', 'Choir', 'Barnabas Chu', 'Pittsburgh', 'Barnabas soup', 'Attunnu', 'Salania', 'apostolic', 'BARNABAS WOLFE', 'Congregation Beth Israel', 'Dr. Barnabas', 'Beth Israel Temple', 'fundraising on Just', 'Brotherhood', 'Mombassa', 'disciples', 'C Barnabas', 'Rehearsal','yonkers', 'healthdigezt.com', 'Camp Barnabas', 'Putnam Community Medical', 'St B\'s', 'Barnabas libray', 'Friends of St Barnabas', 'vs St. Barnabas', 'West Essex', 'barnabas catholic', 'Essential Oils', 'service at St Barnabas', 'on st. Barnabas', 'Epistle', 'my son Barnabas', 'Barnabas Chapel', 'ACW of St.Barnabas', 'StBarnabasLinc', 'UFO', '@NY1', '@BilldeBlasio', 'Kimball Medical Clinic', '#Job alert:', 'bronx', '#NYPDShooting', 'nypd', '#job', '#TweetMyJobs', 'barnabas house','house of barnabas','Barnabas choir','#NowHiring','gospel','Barnabas Grantham','Grantham Hospice','Barnabas College','hymns','volleyball', 'basketball','justgiving','#uk','.uk','#unitedkindom','#england','Lincolnshire','Barnabas Church','Barnabas House','Barnabas Hall','Barnabas High','Barnabas Senior Services','Barnabas Opera','House of St','Barnabas student','on st barnabas','Barnabas Mission','Worship','Warwickshire','Young Living Oils','game at St Barnabas','8th grade','COLLEGE OF ST. BARNABAS','Barnabas Youth Group']
    urls_to_exclude = ['stbarnabastablet', '.uk', 'yuku.com']
    
    # English pound sign content exclusion removed from list so that app can run on matt f's machine unichr(163)
    
    
    #process author related spam rules
    for headline in headlines_to_exclude:
        if headline.upper() in post[1].upper():
            flag = 1
            if flag == 1:
                archive_spam(h, post[0], post[6], 'headline', headline, post[1], post[4])
 
 
    #process author related spam rules
    if not flag == 1:
        for author in authors_to_exclude:
            if author.upper() in post[2].upper():
                flag = 1
                if flag == 1:
                    #send the post to be archived
                    archive_spam(h, post[0], post[6], 'author', author, post[2], post[4])
    
 

    #process content related spam rules
    if not flag == 1:
        for content in content_to_exclude:
            if content.upper() in post[3].upper():
                flag = 1
                if flag == 1:
                    archive_spam(h, post[0], post[6], 'content', content, post[3], post[4])
                
    #process url related spam rules
    if not flag == 1:
        for url in urls_to_exclude:
            if url.upper() in post[4].upper():
                flag = 1
                if flag == 1:
                    archive_spam(h, post[0], post[6], 'url', url, post[4], post[4])


    #return the post if its not spam, our flag its a spam post
    if flag > 0:
        return 1
    else:
        return post
                    
       
        
     
def prep_posts_for_import(hosptial_id, post):
    global headline_table
    
    #add hosptial id to post
    post.insert(0, hosptial_id)

    #article id - remove decial points from article id if they exist
    post[1] = post[1].replace('.00', ' ')
    
    #headline - truncate headlines to be less than 75 character and avoid the headline too long import erro
    post[2] = post[2][:75]
        
    #author should be replaced with 'unknown,' if its blank
    if post[3] =='':
        post[3] = 'Unknown'
    
    #content should not contain commas
    post[4] = post[4].replace(',', ';')
    
    #we need to append a url value after article url
    url = post[5]
    post.insert(6, url)
        
    #fix the date issue by formatting it with zer0
    post[8] = parser.parse(post[8], tzinfos={'EDT' : +18000})
    datetime.strftime(post[8],'[%d/%b/%Y:%H:%M:%S %z]')   
    
    #remove commas from blog_post_engagement
    post[20] = post[20].replace(',', ';')
    
    #swap commas in improt note for semicolons
    post[26] = post[26] = post[26].replace(',', ';')
        
    post[28] = post[28].replace(',', ';')
    
    post[29] = post[29].replace(',', ';')

    return post

def create_post_in_salesforce(post, sf):
	# accepts post, connects to salesforce api via simple-salesforce package and creates the post
	# throws error if the total post counts do not add up after import/post creation
	# as of 7/24 im confidnet this will import new posts, those without dupe urls
	# need to figure out how to catch posts with dupe article urls and handle them
	# need then to catch un caught erros and store them to a file
	# need to validate and report on posts created successfully (by comparing starting sf post count vs exspected)
			
	try:
		sf.Post__c.create({'Hospital__c':post[0], 'Article_Id__c':post[1], 'Name':post[2], 'Content__c':post[4], 'Url__c':post[5], 'Source__c':post[7], 'Publish_Date__c':post[8].isoformat()}) 

	except Exception as inst:
		#create or open an error file
		#add this post to the error file with the error message	

			if 'A post with this url  already exists.' in str(inst):
				#add post to error file with dupe url error message which is str(inst)
				# might be worth checking here for those posts with unique article id but dupe urls. these are likley forum posts on a thread which we lose today and might want to solve for keeping in the future. e.g, if url dupe but artile id not then import. requires removing url verification from salesforce
				print ('dupe url error: ' + post[1])

			elif 'duplicate value found: Article_Id__c' in str(inst):
				#add post to error file with dupe article id error message which is str(inst)
				print ('dupe article id error: ' + post[1])
				
			else:
				#add post to error file with message of error unknow and error message str(inst)
				# consider stopping the import here to prevent hundres of irrelevant posts from getting into the environment
				print ('unknown error', + post[1])
				print str(inst)
						
	return post
	
def main():
    global posts_processed
    global headline_table
    global spam_posts_count

    hosptial_post_count = 0
    hosptial_processed_post_count = 0
    hosptial_spam_post_count = 0


    output_table = PrettyTable()
    spam_count = 0
    
    sf = Salesforce(username='matt@clixlocal.net', password='8@8yd@ddy', security_token='gndMn2mAQA3LGddS3gkaLWe9v')
    print ('Connected to sfdc')



    print('ClixSocial Master File Import Prepper V2 1/3/2015. \n Expects reviewed and tagged R6 csv exports to be in the same directory. \n Collects posts from multiple Radian6 export csv files. \n Builds a single import csv file formatted for Salesforce.com. \n Addresses issue with long post titles creating import errors.  \n Improved user feedback. \n Does not remove spam or auto tag posts. \n \nStarting... \n ')
    time.sleep(1)

    #for each hosptial from list of ids open its rdian file using the id as filename
    Hosptial_ids = ['a03F0000009buV7','a03F0000009Ev1c','a03F0000009Ev1h', 'a03F0000009Ev1N', 'a03F0000009Ev1S','a03F0000009Ev1X', 'a03F0000009EvQQ','a03F0000009FQ7V']    
    
    #make sure post import files are in place
    try:
        for h in Hosptial_ids:
            posts_file = open(h + '.csv','rU')
    except IOError as e:
        print ('Error: Missing Radian file ' + h + '.csv. Please add file to directory and retry.')
        print ('Directory = ' + os.getcwd())
        sys.exit()
    else:
        #create master import file
        master_posts_file = open('masterpostsimport.csv', 'wb')
        post_writer = csv.writer(master_posts_file, delimiter=',')
        post_writer.writerow(['HOSPITAL__C', 'ARTICLE_ID', 'HEADLINE', 'AUTHOR', 'CONTENT', 'ARTICLE_URL', 'URL', 'MEDIA_PROVIDER', 'PUBLISH_DATE', 'VIEW_COUNT', 'COMMENT_COUNT', 'UNIQUE_COMMENTERS', 'ENGAGEMENT', 'LIKES_AND_VOTES', 'INBOUND_LINKS', 'FORUM_THREAD_SIZE', 'FOLLOWING', 'FOLLOWERS', 'UPDATES', 'BLOG_POST_SENTIMENT', 'BLOG_POST_ENGAGEMENT', 'BLOG_POST_CLASSIFICATION', 'BLOG_POST_ASSIGNMENT', 'BLOG_POST_PRIORITY', 'BLOG_POST_COMMENT', 'BLOG_POST_NOTE', 'BLOG_POST_TAG', 'BLOG_SOURCE_TAG', 'FIRST_ENGAGEMENT_ACTIVITY', 'LAST_ENGAGEMENT_ACTIVITY'])
        output_table.field_names = ['HOSPITAL ID', 'PROCESSED', 'SPAM', 'ADDED TO IMPORT FILE']
        
        for h in Hosptial_ids:
            posts_file = open(h + '.csv','rU')
            hosptial_post_count = sum(1 for row in posts_file) - 1
            hosptial_spam_post_count = 0
            hosptial_processed_post_count = 0
            posts_file.close()
            
            posts_file = open(h + '.csv','rU')
            posts = csv.reader(posts_file)
                                               
            #count the number of posts in reader and send that to status                                                                            
            for post in posts:
                if not 'ARTICLE_ID' in post: 
                    spam_flag = remove_spam(h, post)
                    if spam_flag == 1:
                        spam_count = spam_count + 1
                        hosptial_spam_post_count = hosptial_spam_post_count + 1
                        hosptial_processed_post_count = hosptial_processed_post_count + 1 
                        hosptial_post_count = hosptial_post_count - int(spam_flag)
                    else:
                        prep_posts_for_import(h, post)
                        post_writer.writerow(post)
                        create_post_in_salesforce(post, sf)
                        posts_processed = posts_processed + 1
                        hosptial_processed_post_count = hosptial_processed_post_count + 1 

            output_table.add_row([h, hosptial_processed_post_count, hosptial_spam_post_count, hosptial_post_count])
                                                                          
        #close files, archive numbers and provide user feedback
        posts_file.close()
        master_posts_file.close()
        
        print ('spam highlights')
        
        print ('Operation complete.')
        print (str(spam_posts_count) + ' spam items removed.')
        print (str(posts_processed) + ' posts added to master import file.')
        print ('Remember to review spam posts archive to ensure that no posts were removed in error.')
        
        # there should be a check here that the number of rows in the maser import file less the header matches posts process less spam (this would ensure we arent missinay anything)
        
        #print (headline_table)
        print(output_table)
             
if __name__ == "__main__":
  main()
