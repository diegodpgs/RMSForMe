import os
from config import *


#TODO verify files new.movies and new_movies.title
def init_verify():
	test_srt_movies_file = os.listdir(os.getcwd()+'/'+FOLDER_SRT_TEST)
	
	if '.DS_Store' in test_srt_movies_file:
		test_srt_movies_file = test_srt_movies_file[1:]


	# TRAIN_UTTERANCE = os.listdir(os.getcwd()+'/'+FOLDER_UTTERANCE_TRAIN)
	# if '.DS_Store' in TRAIN_UTTERANCE:
	# 	TRAIN_UTTERANCE = TRAIN_UTTERANCE[1:]
	# TRAIN_UTTERANCE = ['tt'+i.split('_tt')[1].split('.')[0] for i in TRAIN_UTTERANCE]

	# TEST_UTTERANCE = os.listdir(os.getcwd()+'/'+FOLDER_UTTERANCE_TEST)
	# if '.DS_Store' in TEST_UTTERANCE:
	# 	TEST_UTTERANCE = TEST_UTTERANCE[1:]
	# TEST_UTTERANCE = ['tt'+i.split('_tt')[1].split('.')[0] for i in TEST_UTTERANCE]

	test_srt_movies_file = ['tt'+i.split('_tt')[1].split('.')[0] for i in test_srt_movies_file]


	TRAIN_SRT = os.listdir(os.getcwd()+'/'+FOLDER_SRT_TRAIN)
	TRAIN_SRT = ['tt'+i.split('_tt')[1].split('.')[0] for i in TRAIN_SRT]


	# TEST_TAG = os.listdir(os.getcwd()+'/'+FOLDER_TEST_TAGS)
	# TEST_TAG = ['tt'+i.split('_tt')[1].split('.')[0] for i in TEST_TAG[1:]]

	# TRAIN_TAG = os.listdir(os.getcwd()+'/'+FOLDER_TRAIN_TAGS)
	# TRAIN_TAG = ['tt'+i.split('_tt')[1].split('.')[0] for i in TRAIN_TAG[1:]]

	# train_cast_file = open(PATH__WATCHED_CAST)
	# TRAIN_CAST = dict([(t.split(';')[0],";".join(t.split(';')[1:])) for t in train_cast_file.read().split('\n')])
	# train_cast_file.close()

	# test_cast_file = open(PATH__NEW_CAST)
	# TEST_CAST = dict([(t.split(';')[0],";".join(t.split(';')[1:])) for t in test_cast_file.read().split('\n')])
	# test_cast_file.close()

	watched_movies = open(PATH__WATCHED_MOVIES).read().split('\n')
	movies_name = []
	movies_name.extend([(i.split(';')[0],i.split(';')[1]) for i in open(PATH__NEW_MOVIES).read().split('\n')])
	movies_name.extend([(w.split(';')[1],w.split(';')[0]) for w in watched_movies])
	movies_name = dict(movies_name)

	new_movies = open(PATH__NEW_MOVIES_CODE)


	NM = new_movies.read().split('\n')
	WM = [w.split(';')[0] for w in watched_movies]
	new_movies.close()
	

	verify_srt(TRAIN_SRT,
				test_srt_movies_file,
				NM,
				WM,
				movies_name)



	# verify_cast(TRAIN_CAST,TEST_CAST,NM,WM)
	# verify_utterances(TRAIN_UTTERANCE,TEST_UTTERANCE,NM,WM)

#CONCLUDED
def verify_srt(srt_train,srt_test,new_movies_list,watched_movies_list,dic_movies):
	"""
		srt_train,srt_test,watched_movies_list,new_movies:  [list of IMDB code]
		dic_movies: a dicionary that maps IMDB_code to movie title

		What is verifying?
			srt_train
			srt_test

		Verify if
		- there are srt file duplicated in test and train
		- a file labeled as test was not watched yet
		- a file labeled as train was already watched
		- there are srt file to download

	"""

	for srt_imdb_code in srt_test:
		if srt_imdb_code in new_movies_list and srt_imdb_code in watched_movies_list:
			print '%s/%s was already watched. It was removed from new movie list' % (dic_movies[srt_imdb_code],srt_imdb_code)
			new_movies_list.remove(srt_imdb_code)

		elif srt_imdb_code not in new_movies_list and srt_imdb_code not in watched_movies_list:
			print '%s/%s is not in new movies list and watched movies list' % (dic_movies[srt_imdb_code],srt_imdb_code)

		elif srt_imdb_code in srt_train:
			print '%s/%s/test must to be removed from TEST/database' % (dic_movies[srt_imdb_code],srt_imdb_code) 

	for srt_imdb_code in srt_train:
		
		if srt_imdb_code in new_movies_list and srt_imdb_code in watched_movies_list:
			print '%s/%s was already watched. It was removed from new movie list' % (dic_movies[srt_imdb_code],srt_imdb_code)
			new_movies_list.remove(srt_imdb_code)

		elif srt_imdb_code not in new_movies_list and srt_imdb_code not in watched_movies_list:
			print '%s/%s is not in new movies list and watched movies list' % (dic_movies[srt_imdb_code],srt_imdb_code)



	for imdb_code in new_movies_list:
		if imdb_code not in srt_test:
			if imdb_code not in dic_movies:
				print '%s srt file must to be Downloaded to TEST' % (imdb_code)
			else:
				print '%s/%s srt file must to be Downloaded to TEST' % (dic_movies[imdb_code],imdb_code)

	for code_movie in watched_movies_list:
		if code_movie not in srt_train and code_movie not in srt_test:
			if imdb_code not in dic_movies:
				print '%s srt file must to be Downloaded to TRAIN' % (imdb_code)
			else:
				print '%s/%s srt file must to be Downloaded to TRAIN' % (dic_movies[imdb_code],imdb_code)
		elif code_movie not in srt_train:
			print '%s/%s must to be copied from srt_test to TRAIN' % (dic_movies[imdb_code],imdb_code)

	fnew_movie_titles = open(PATH__NEW_MOVIES_CODE,'w')

	for index in xrange(len(new_movies_list)):
		i = new_movies_list[index]
		fnew_movie_titles.write(i)
		if index < len(new_movies_list)-1:
			fnew_movie_titles.write('\n')

	print 'The new_movie_list was updated'

# #def verify_tag():

# #CONCLUDED
# def verify_utterances(utterance_train,utterance_test,new_movies_list,watched_movies_list):
# 	"""
# 		cast_train,cast_test,new_movies_list,watched_movies_list  list<imdb_code>
# 	"""
# 	output = ''

# 	for utterance_file in utterance_test:
# 		if utterance_file in watched_movies_list:
# 			if utterance_file in new_movies_list:
# 				new_movies_list.remove(utterance_file)
# 			else:
# 				output += 'test\\%s copy to train\n' % utterance_file


# 		elif utterance_file not in new_movies_list and utterance_file not in watched_movies_list:
# 			output += 'test\\%s not in new.movies\n' % utterance_file

# 	for utterance_file in utterance_train:
		
# 		if utterance_file not in new_movies_list and utterance_file not in watched_movies_list:
# 			output += 'train\\%s not in watched.movies\n' % utterance_file

# 	for code_movie in new_movies_list:
# 		if code_movie not in utterance_test:
# 			output += 'Convert utterance_file %s to test\n' % code_movie

# 	for code_movie in watched_movies_list:
# 		if code_movie not in utterance_train and code_movie not in utterance_test:
# 			output += 'Download utterance_file %s to train\n' % code_movie
# 		elif code_movie not in utterance_train:
# 			output += 'Copy utterance_file %s from test\n' % code_movie

# 	fnew_movie_titles = open(PATH__NEW_MOVIES_CODE,'w')

# 	for index in xrange(len(new_movies_list)):
# 		i = new_movies_list[index]
# 		fnew_movie_titles.write(i)
# 		if index < len(new_movies_list)-1:
# 			fnew_movie_titles.write('\n')

# 	if output != '':
# 		raise Exception('\n'+output)
	
# #CONCLUDED
# def verify_cast(cast_train,cast_test,new_movies_list,watched_movies_list):

# 	"""
# 		cast_train,cast_test,new_movies_list,watched_movies_list  list<imdb_code>
# 	"""
# 	output = ''
# 	TEST_CAST_ITERATOR = list(cast_test.items())
# 	TRAIN_CAST_ITERATOR = list(cast_train.items())

# 	for cast_file in TEST_CAST_ITERATOR:
		
# 		cast_file = cast_file[0]

# 		if cast_file in new_movies_list and cast_file in watched_movies_list:
# 			new_movies_list.remove(cast_file)

# 		elif cast_file not in new_movies_list and cast_file not in watched_movies_list:
# 			output += 'test\\%s not in new.movies\n' % cast_file
# 			del cast_test[cast_file]


# 	for cast_file in TRAIN_CAST_ITERATOR:
# 		cast_file = cast_file[0]

# 		if cast_file not in new_movies_list and cast_file not in watched_movies_list:
# 			output += 'train\\%s not in watched.movies\n' % cast_file

# 	for code_movie in new_movies_list:
# 		if code_movie not in cast_test:
# 			output += 'Download cast_file %s to test\n' % code_movie

# 	for code_movie in watched_movies_list:
# 		if code_movie not in cast_train and code_movie not in cast_test:
# 			output += 'Download cast_file %s to train\n' % code_movie
# 		elif code_movie not in cast_train and code_movie in cast_test:
# 			output += 'Copy cast_file %s from test\n' % code_movie
# 			cast_train[code_movie ] = cast_test[code_movie ]
# 			del cast_test[code_movie ]

# 	fnew_movie_titles = open(PATH__NEW_MOVIES_CODE,'w')

# 	for index in xrange(len(new_movies_list)):
# 		i = new_movies_list[index]
# 		fnew_movie_titles.write(i)
# 		if index < len(new_movies_list)-1:
# 			fnew_movie_titles.write('\n')

	
	
# 	cast_test_writer = open(PATH__NEW_CAST,'w')
# 	for key,stars in cast_test.iteritems():
# 		cast_test_writer.write('%s;%s\n' % (key,stars))

# 	cast_train_writer = open(PATH__WATCHED_CAST,'w')
# 	for key,stars in cast_train.iteritems():
# 		cast_train_writer.write('%s;%s\n' % (key,stars))

	
# 	if output != '' and '\ ' not in output:
# 		raise Exception('\n'+output)


init_verify()



