"""
COR: 0.0925
VARIANCE: 1.1004
DESVIO: 1.0480

RELEVANCE_SCORE:  0.08806

"""
import os
import nltk
from shutil import copyfile
import urllib2
import os
from environment import *


def getTags(title_code): 	
					
	link = urllib2.urlopen('http://www.imdb.com/title/%s/keywords' % title_code).readlines()
	tags = {}
	
	
	for index in xrange(500,len(link)):
		line = link[index]
	
		if 'this relevant' in line:
			out = 0
			total = 0
		
			if 'found' in line:
				out =  int(line.split('of')[0].split('>')[1])
				total = int(line.split('of')[1].split('found')[0])
		

			word = link[index-5].split('</a>')[0].split('>')[1]
			word = word.replace(' ','_')
			tags[word] = (out,total)
	return tags

def catchTags():
	watched_movies = open(FILE_WATCHED_DATA).read().split('\n')
	watched_movies = dict([(i.split(';')[0],i.split(';')[1]) for i in watched_movies])
	watchlist_movies = open(FILE_WATCHLIST_DATA).read().split('\n')
	watchlist_movies = dict([(i.split(';')[0],i.split(';')[1]) for i in watchlist_movies])


	test_tag_movies_file = os.listdir(os.getcwd()+'/'+FOLDER_TAG_TEST)
	test_tag_movies_file = ['tt'+i.split('_tt')[1].split('.')[0] for i in test_tag_movies_file[1:]]

	train_tag_movies_file = os.listdir(os.getcwd()+'/'+FOLDER_TAG_TRAIN)
	train_tag_movies_file = ['tt'+i.split('_tt')[1].split('.')[0] for i in train_tag_movies_file[1:]]

	
	for code_imdb,movie_name in watchlist_movies.iteritems():
		if code_imdb not in test_tag_movies_file:
			
			tags = getTags(code_imdb)
			tags_writer = open('%s/%s_%s.tags' % (FOLDER_TAG_TEST,movie_name,code_imdb),'w')
			for key,values in tags.iteritems():
				tags_writer.write('%s;#;%d;#;%d\n' % (key,values[0],values[1]))
			print 'Tag',code_imdb,'test processed'

	for code_imdb,movie_name in watched_movies.iteritems():
		if code_imdb not in train_tag_movies_file:
			
			tags = getTags(code_imdb)
			tags_writer = open('%s/%s_%s.tags' % (FOLDER_TAG_TRAIN,movie_name,code_imdb),'w')
			for key,values in tags.iteritems():
				tags_writer.write('%s;#;%d;#;%d\n' % (key,values[0],values[1]))
			print 'Tag',code_imdb,'train processed'

def trainTags():
	movies_ranked = open(FILE_WATCHED_DATA).read().split('\n')
	movies = dict([(m.split(';')[0],int(m.split(';')[4])) for m in movies_ranked])
	score_tags = {}
	path = os.getcwd()+'/'+FOLDER_TAG_TRAIN
	files = os.listdir(path)

	if '.DS_Store' in files:
		files.remove('.DS_Store')

	for tag_file in files:
		tag_data = open(path+'/'+tag_file).read().split('\n')
		
		if '_' not in tag_file:
			tag_movie = tag_file.split('.t')[0]
		else:
			tag_movie = tag_file.split('_')[-1].split('.t')[0]
		
		for tag_line in tag_data[:-1]:

			tag = tag_line.split(';#;')[0]
			c1 = int(tag_line.split(';#;')[1])
			c2 = int(tag_line.split(';#;')[2])

			if (c1 >= c2 or c1 >= 2) and (tag_movie in movies):
				if tag not in score_tags:
					score_tags[tag] = []
				for i in xrange(c1+1):
					score_tags[tag].append(movies[tag_movie])

	tag_file = open(FILE_TRAIN_TAG,'w')
	for tag,scores in score_tags.iteritems():
		tag_file.write('%s;%1.2f\n' % (tag,sum(scores)/float(len(scores))))

	tag_file.close()
	print 'TAGS_TRAIN_PROCESSED'

def testTags():
	score_movies = {}
	path = os.getcwd()+'/'+FOLDER_TAG_TEST
	files = os.listdir(path)
	tags_train = open(FILE_TRAIN_TAG).read().split('\n')
	tags_train = dict([(t.split(';')[0],float(t.split(';')[1])) for t in tags_train[0:-1]])
	best_tags = {}

	if '.DS_Store' in files:
		files.remove('.DS_Store')

	for tag_file in files[:-1]:

		tag_data = open(path+'/'+tag_file).read().split('\n')
		tag_movie = tag_file.split('_')[-1].split('.t')[0]
		tags_tokens = []
		added = 5
		for tag_line in tag_data[:-1]:

			tag = tag_line.split(';#;')[0]
			c1 = int(tag_line.split(';#;')[1])
			c2 = int(tag_line.split(';#;')[2])

			tags_tokens.extend(tag.split('_'))



			if (c1 >= c2 and c1 > 0) and tag in tags_train:
				if tag_movie not in score_movies:
					score_movies[tag_movie] = []
				for i in xrange(c1+1):
					score_movies[tag_movie].append(tags_train[tag])

				added -= 1

		if added > 0:
			index = 0
			while index < len(tag_data)-1 and added > 0:
				tag_line = tag_data[index]
				tag = tag_line.split(';#;')[0]
				c1 = int(tag_line.split(';#;')[1])
				c2 = int(tag_line.split(';#;')[2])

				if tag in tags_train:
					if tag_movie not in score_movies:
						score_movies[tag_movie] = []
					for i in xrange(c1+1):
						score_movies[tag_movie].append(tags_train[tag])
					added -= 1
				index += 1
		best_tags[tag_movie] = []
		freq_tags = nltk.FreqDist(tags_tokens)
		index_tags_frequency = 0
		most_common = freq_tags.most_common(100)
		index_mc = 0
		prepositions = ['aboard', 'about', 'above', 'across', 'after', 'against', 'along', 'amid', 'among', 'anti', 'around', 'as', 'at', 'before', 'behind', 'below', 'beneath', 'beside', 'besides', 'between', 'beyond', 'but', 'by', 'concerning', 'considering', 'despite', 'down', 'during', 'except', 'excepting', 'excluding', 'following', 'for', 'from', 'in', 'inside', 'into', 'like', 'minus', 'near', 'of', 'off', 'on', 'onto', 'opposite', 'outside', 'over', 'past', 'per', 'plus', 'regarding', 'round', 'save', 'since', 'than', 'through', 'to', 'toward', 'towards', 'under', 'underneath', 'unlike', 'until', 'up', 'upon', 'versus', 'via', 'with', 'within', 'without']
		pronouns = ['name','one','no','not','i', 'am', 'you', 'yours', 'their', 'theirs', 'him', 'her', 'mine', 'yours', 'to', 'a', 'we', 'ours','the','title','character','new']
		while index_tags_frequency <= 3:
			if len(most_common) == 0:
				print '%s has empty tag' % tag_file
				break
			mc = most_common[index_mc][0]
			index_mc += 1

			#if mc not in prepositions and mc not in pronouns:
			index_tags_frequency += 1
			best_tags[tag_movie].append(mc)

		

	tag_file = open(FILE_TEST_TAG,'w')
	movie_dic = dict([(i.split(';')[0],i.split(';')[1]) for i in open(FILE_WATCHLIST_DATA).read().split('\n')])
	for imdb_code,scores in score_movies.iteritems():
		scores.sort()
		if len(scores) > 3:
			del scores[0]
			del scores[-1]
		
		#tag_file.write('%s;%1.2f\n' % (tag,sum(scores)/float(len(scores))))
		if imdb_code not in movie_dic:
			print '%s is in tag/test, but not in watchlist.data' % imdb_code
			continue
		tag_file.write('%s;%1.2f' % (movie_dic[imdb_code],scores[len(scores)/2]))
		for t in best_tags[imdb_code]:
			tag_file.write(';%s' % t)
		tag_file.write('\n')
		
	print 'TAGS_TEST_PROCESSED'
	tag_file.close()

def runTags():
	catchTags()
	trainTags()
	testTags()
	#print '________TAGS PROCESSED________'

runTags()




