#coding: UTF-8
import urllib2
import sys
import os
import math
from environment import *
sys.path.insert(0,os.getcwd()+'/data')
from data import *

class Cast:

	def __init__(self):
		self.map_star_to_imdbcode = self.map_star_imdb()

	def map_star_imdb(self):
		m = {}
		for movie_cast in open(FILE_WATCHED_CAST).read().split('\n'):
			imdb_code = movie_cast.split(';')[0]
			stars = movie_cast.split(';')[2:]
			for star in stars:
				if star not in m:
					m[star] = []

				if imdb_code not in m[star]:
					m[star].append(imdb_code)
		return m

	# def getCast(self,movie_url):
	# 	"""
	# 	 Retrieval Cast from IMDB
	# 	"""
	# 	cast = []

	# 	movie_page	= urllib2.urlopen(movie_url).readlines()
		
	# 	for index in xrange(5,len(movie_page)):
			
	# 		if '<h1 class="header">' not in movie_page[index] and '/company/' not in movie_page[index-1]:
	# 			if '<span class="itemprop" itemprop="name">' in movie_page[index]:
	# 				name = movie_page[index].split('<span class="itemprop" itemprop="name">')[1].split('<')[0]
				
	# 				if name not in cast:
	# 					cast.append(name)
					
	# 	return cast

	# def write_cast(self,cast_data_file,movies_data_file):

	# 	cast = None
	# 	cast_movies_extracted = []

	# 	try:
	# 		cast = open(cast_data_file)
	# 		cast_movies_extracted = [i.split(';')[0] for i in cast.read().split('\n')]
	# 		cast.close()
	# 	except:
	# 		cast = open(cast_data_file,'w')
	# 		cast.close()
		
	# 	movies_data = dict([(i.split(';')[0],i.split(';')[1]) for i in open(movies_data_file).read().split('\n')])
	# 	cast_scores = {}

	# 	cast_db = open(cast_data_file,'a')

	# 	for imdb_code,title in movies_data.iteritems():
			
	# 		if imdb_code not in cast_movies_extracted:
	# 			cast = getCast('http://www.imdb.com/title/%s/' % imdb_code)
				
	# 			cast_db.write('%s;%s' % (imdb_code,title))
				
	# 			for c in cast:
	# 				cast_db.write(';%s' % c)
	# 			cast_db.write('\n')
				
	# 			print 'Cast %s/%s processed' % (imdb_code,title)

	# 	cast_db.close()

	# def crawly_cast(self):
	# 	"""
		   
	# 	   Retrieval the cast movies from IMDB.com

	# 	"""

	# 	write_cast(FILE_WATCHED_CAST,FILE_WATCHED_DATA)
	# 	write_cast(FILE_WATCHLIST_CAST,FILE_WATCHLIST_DATA)

	# def train_cast(self):
	# 	"""
	# 		level1: 0:4 first stars
	# 		level2: 5:10 first stars
	# 		level3: >10 after the first 10 stars
	# 		[star] = {'stantard':X,'N1':X,'N2':X,'N3':X,{'Comedy':x, 'Drama':X ....}}

	# 		Use my ranting in each movie to compute the score
	# 		For instance
	# 		Nicolas Cage
	# 			tt0448011;knowing;7
	# 			tt0368891;national_treasure;8
	# 			tt0963966;the_sorcerer_s_apprentice;4
	# 			tt0120632;city_of_angels;9
	# 			tt0399295;lord_of_war;9
	# 			tt0814022;bangkok_dangerous;7
	# 			tt0259324;ghost_rider;6

	# 			(this is computed by Levels)
	# 			Average 7.14
	# 			Standardized: 7.4 (remove the highest and lowest score)
	# 				REMOVE tt0963966;the_sorcerer_s_apprentice;4
	# 				REMOVE tt0399295;lord_of_war;9

	# 			Beyond that is computed the overall score for each genre

	# 	"""
	# 	#imdb_code;star1;star2....
	# 	stars = open(FILE_WATCHED_CAST).read().split('\n')[:-1]

	# 	#[imdb_code] = [my_score,title,[genre1,genre2,genre3]]
	# 	watched_data = open(FILE_WATCHED_DATA).read().split('\n')

	# 	movies_data = {}
	# 	for movie_data in watched_data:
	# 		imdb_code = movie_data.split(';')[0]
	# 		my_rating = float(movie_data.split(';')[4])
	# 		title = movie_data.split(';')[1]
	# 		genres = movie_data.split(';')[5:]
	# 		movies_data[imdb_code] = {'my_rating':my_rating,
	# 								  'title':title,
	# 								  'genres':genres}


	# 	star_train_writer = open(FILE_TRAIN_CAST,'w')
	# 	stars_data = {}
	# 	for movie_cast_data in stars[:-1]:
	# 		sp = movie_cast_data.split(';')
	# 		cast_movie = sp[2:]
	# 		imdb_code = sp[0]
	# 		title = movies_data[imdb_code]['title']
			
	# 		if imdb_code not in movies_data:
	# 			raise Exception('The movie %s is not in watched.movies. Remove from watched.cast' % title)

	# 		my_rating =  movies_data[imdb_code]['my_rating']
	# 		genres_movie = movies_data[imdb_code]['genres']
				

	# 		for index in xrange(len(cast_movie)):
	# 			star = cast_movie[index]

	# 			level = 'N3'
	# 			if index < 5:
	# 				level = 'N1'
	# 			elif index < 10:
	# 				level = 'N2'

	# 			if star not in stars_data:
					
	# 				stars_data[star] = {}
	# 				stars_data[star][level] = {}
	# 				for genre in GENRES:
	# 					stars_data[star][level][genre] = []
	# 				stars_data[star][level]['_OVERALL_'] = []

	# 			elif level not in stars_data[star]:
	# 				stars_data[star][level] = {}
	# 				for genre in GENRES:
	# 					stars_data[star][level][genre] = []
	# 				stars_data[star][level]['_OVERALL_'] = []
					

	# 			stars_data[star][level]['_OVERALL_'].append(my_rating)

	# 			for genre in genres_movie:
	# 				#print genre,stars_data[star][level]
	# 				stars_data[star][level][genre].append(my_rating)
			
			
	# 	star_train_writer.write('star;N1;N2;N3;total_movies;raw_score')
	# 	for g in GENRES:
	# 		star_train_writer.write(';%s' % g)
	# 	star_train_writer.write('\n')


	# 	for star, levels in stars_data.iteritems():
	# 		star_train_writer.write('%s;' % (star))

	# 		if len(star)<=1:
	# 			continue #To avoid store stars without names
	# 		movies_registered = 0
	# 		raw_score = []

	# 		for level in ['N1','N2','N3']:
	# 			if level not in levels:
	# 				star_train_writer.write('0.0;')
	# 				continue
	# 			data = levels[level]
	# 			scores = data['_OVERALL_']
	# 			score_sum =  sum([d for d in scores])
	# 			score_count = len(scores)
	# 			score_average = score_sum/float(score_count)
	# 			standard_score = score_average
	# 			movies_registered += score_count

	# 			if len(scores) > 3:
	# 				min_score = min(scores)
	# 				max_score = max(scores)
	# 				standard_score = (score_sum-(min_score+max_score))/(score_count-2.0)

	# 			star_train_writer.write('%1.2f;' % standard_score)
	# 			raw_score.extend(scores)


	# 		star_train_writer.write('%d;%1.2f' % (movies_registered,sum(raw_score)/len(raw_score)))
			
	# 		for genre in GENRES:
	# 			scores = []
	# 			if 'N1' in stars_data[star]:
	# 				scores = stars_data[star]['N1'][genre]
	# 			if 'N2' in stars_data[star]:
	# 				scores.extend(stars_data[star]['N2'][genre])
	# 			if 'N3' in stars_data[star]:
	# 				scores.extend(stars_data[star]['N3'][genre])
	# 			if len(scores) > 1:
	# 				average = sum(scores)/len(scores)
	# 				star_train_writer.write(';%1.2f' % average)
	# 			else:
	# 				star_train_writer.write(';0.0')
	# 		star_train_writer.write('\n')

	def getExperienceScore(self,cast):
		experience = set([])

		for star in cast:
			if star in self.map_star_to_imdbcode:
				new = set(self.map_star_to_imdbcode[star])
				experience = experience.union(new)


		"""The values below were obtained by the following statistics
			experience is computed by the number of movies a all stars have made
		    Level 5 >= 13  10 percentil
		    Level 4 >= 09  First quartil 25%
		    Level 3 >= 05  Median
		    Level 2 >= 01  Third quartil 75%
		    Level 1 >= 00  90 percentil
		"""
		experience = len(experience)
		if experience >= 13:
			return (experience,5)
		elif experience >= 9:
			return (experience,4)
		elif experience >= 5:
			return (experience,3)
		elif experience >= 1:
			return (experience,2)
		return (experience,1)

	def computeNScore(self,train,data,N):
		score = []
		for star in data[N]:
			if star in train:
				nscore = train[star][N]
				if nscore != 0:
					score.append(nscore)

		if len(score) == 0:
			return  0.0
		else:
			return sum(score)/len(score)

	def test_cast(self):
		"""
		Experince: the set of  total of movies made by the stars
		compute stars scores by level
		N1 = 0.6
		N2 = 0.3
		N3 = 0.1

		stars1 = N1:8    N2:7   N3:
		stars2 = N1:9    N2:0   N3:8
		stars3 = N1:5    N2:0   N3:7

		newmovie: 
		N1: star1
		N2: star2
		N3: star3

		score = 8*.6 + 0(remove) + 7*.1
		score = (48 + 7)/7 ==> 7.85	
		"""

		test_writer = open(FILE_TEST_CAST).read().split('\n')
		test_movies = open(FILE_WATCHLIST_DATA).read().split('\n')
		test_cast = open(FILE_WATCHLIST_CAST).read().split('\n')
		test_writer = open(FILE_TEST_CAST,'w')
		test_data = {}

		for movie_data in test_movies:
			imdb_code = movie_data.split(';')[0]
			test_data[imdb_code] = {'title':movie_data.split(';')[1],
									'genres':movie_data.split(';')[9:]}

		for cast in test_cast[0:-1]:
			imdb_code = cast.split(';')[0]
			stars = cast.split(';')[2:]
			N1 = stars[0:min(4,len(stars))]
			N2 = []
			N3 = []
			if len(stars) > 6:
				N2 = stars[4:min(10,len(stars))]
			if len(stars) > 12:
				N3 = stars[10:]

			test_data[imdb_code]['N1'] = N1
			test_data[imdb_code]['N2'] = N2
			test_data[imdb_code]['N3'] = N3

		train_cast_data = open(FILE_TRAIN_CAST).read().split('\n')
		train_data = {}


		for cast_data in train_cast_data[1:-1]:
			star_name = cast_data.split(';')[0]
			genres_movie = cast_data.split(';')[6:]
			train_data[star_name] = {'N1':float(cast_data.split(';')[1]),
									 'N2':float(cast_data.split(';')[2]),
									 'N3':float(cast_data.split(';')[3]),
									 'total_movies':int(cast_data.split(';')[4]),
									 'raw_score':float(cast_data.split(';')[5])}
			for index in xrange(len(genres_movie)):
				if genres_movie[index] > 0.0:
					train_data[star_name][GENRES[index]] = genres_movie[index]


		test_writer.write('title;N1;N2;N3;total_movies;level;overall_score;genres\n')
		for imdb_code, data in test_data.iteritems():
			stars = data['N1']
			stars.extend(data['N2'])
			stars.extend(data['N3'])
			experience = self.getExperienceScore(stars)
			N1 = self.computeNScore(train_data,data,'N1')
			N2 = self.computeNScore(train_data,data,'N2')
			N3 = self.computeNScore(train_data,data,'N3')
			

			
			#Evaluate movie only if has the cast have made at least 3 movies
			overall_score = 0.0
			if experience[0] >= 3:
				 if N1*N2*N3 >0 :
				 	overall_score = (N1*.6+N2*.3+N3*.1)*.8+(5+experience[1])*.2
				 elif N1*N2 > 0:
				 	overall_score = (N1*.75+N2*.25)*.8+(5+experience[1])*.2
				 elif N1*N3 > 0:
				 	overall_score = (N1*.85+N2*.15)*.8+(5+experience[1])*.2
				 elif N1 >= 0:
				 	overall_score = N1*.8+(5+experience[1])*.2
				 else:
				 	overall_score = 0.0

			
			test_writer.write('%s;%1.2f;%1.2f;%1.2f;%d;%d;%1.2f\n' % (data['title'],
												  N1,N2,N3,experience[0],experience[1],overall_score))






		# new_movies_stars = open(PATH__NEW_CAST).read().split('\n')
		# movies_cast = dict([(m.split(';')[0],m.split(';')[1:]) for m in new_movies_stars])
		# genres_code = dict([(g.split(';')[0],int(g.split(';')[1])) for g in open(PATH__GENRES_CODE).read().split('\n')])
		# test_cast_writer = open(PATH__STAR_TEST_SCORE,'w')
		

		# #star;overall_score;standard_score;movies;Sci-Fi;Crime;Romance;Animation;Music;Comedy;War;Horror;Adventure;Thriller;Western;Mystery;Short;Drama;Action;Documentary;Musical;History;Family;Fantasy;Sport;Biography

		# test_cast_writer.write('imdb_code;title;general_score;famous_cast#genres#genres_score\n')
		# for title,stars in movies_cast.iteritems():
		# 	if title == '': #GAMBIARRA
		# 		continue
		# 	movie_cast_score = []
		# 	movie_cast_score_genre = {}
		# 	movies_made = 0
		# 	genres_complemento = 0 #numero de generos para completar os 3 minimos
		# 						   #se este valor for maior que 1 a nota e duplicada
		# 						   #ex.   score 7, drama;crime;
		# 						   #      drama[7,7] crime[7,7]
		# 						   #    
		# 						   #      score 7 drama;;
		# 						   #	  drama[7,7,7]

		# 	for star in stars:
				

		# 		if star not in train_cast:
		# 			continue
		# 		score_star = max(float(train_cast[star][0]),float(train_cast[star][1]))
		# 		movie_cast_score.append(score_star)
		# 		genres = train_cast[star][3:]
				
		# 		movies_made += float(train_cast[star][2])
		# 		for genre in genres_new_movies[title]:
		# 			if genre == '':
		# 				genres_complemento += 1
		# 				continue
					
		# 			genre_score = float(genres[genres_code[genre]-1])

		# 			if genre not in movie_cast_score_genre:
		# 				movie_cast_score_genre[genre] = []

		# 			if genre_score > 0:
		# 				movie_cast_score_genre[genre].append(genre_score)

		# 		for genre,scores in movie_cast_score_genre.iteritems():
		# 			if len(scores)> 1:
		# 				for i in xrange(genres_complemento):
		# 					movie_cast_score_genre[genre].append(movie_cast_score_genre[genre][-1])



		# 	#COMPUTE SCORES
		# 	movies_made = movies_made/len(stars)
		# 	if len(movie_cast_score) == 0:
		# 		movie_cast_score = 0	
		# 	else:
		# 		movie_cast_score = sum(movie_cast_score)/len(movie_cast_score)
		# 	movie_cast_score_genre = zip(movie_cast_score_genre.keys(),movie_cast_score_genre.values())

		# 	movie_cast_score_genre.sort()

		# 	test_cast_writer.write('%s;%s;%1.2f;%1.3f#' % (title,new_movies_titles[title],movie_cast_score,movies_made))
			
		# 	movie_cast_score_genre_final = []
		# 	for index in xrange(max(4,len(movie_cast_score_genre))):
				
		# 		if index < len(movie_cast_score_genre):
		# 			g = movie_cast_score_genre[index]
		# 		else:
		# 			g = ['NA',[]]
		# 		if len(g[1]) == 0:
		# 			test_cast_writer.write('%s;0.0;' % (g[0]))
		# 		else:
		# 			test_cast_writer.write('%s;%1.2f;' % (g[0],sum(g[1])/len(g[1])))
		# 			movie_cast_score_genre_final.append(sum(g[1])/len(g[1]))

			
		# 	score_final = 0
		# 	if len(movie_cast_score_genre_final) > 0:
		# 		score_final = sum(movie_cast_score_genre_final)/len(movie_cast_score_genre_final)
		# 	test_cast_writer.write('%1.2f\n' % score_final)


		# 	if title not in genres_movies:
		# 		print 'Title: "%s" movie has already watched. Remove register from new.cast' % title
		# 		wc = open(PATH__WATCHED_CAST,'a')
		# 		if len(title)>2:
		# 			wc.write('%s;%s\n' % (title,";".join(cast)))
		# 		wc.close()
		# 		continue
		# 	name = genres_movies[title][0]
		# 	score_genres = {}
		# 	score_overal = []

		# 	for g in genres_movies[title][5:]:
		# 		if g not in genres_code and g != 'NA':
		# 			raise Exception('%s:Genre %s does not exist' % (title,g))
		# 		elif g != 'NA':
		# 			cast_new_movie = movies_cast[title]
		# 			score_genres[g] = []
					
		# 			for star in cast_new_movie:
		# 				if star in train_cast:
							
		# 					score = float(train_cast[star][genres[g]])
		# 					if score != 0:
		# 						score_genres[g].append(float(score))
		# 					score_overal.append(float(train_cast[star][0]))
		# 			if len(score_genres[g]) == 0:
		# 				score_genres[g] = 0
		# 			else:
		# 				score_genres[g] = sum(score_genres[g])/len(score_genres[g])
			
		# 	if len(score_overal) == 0:
		# 		sf.write('%s;%s;0' % (title,name))
		# 	else:
		# 		sf.write('%s;%s;%1.2f' % (title,name,sum(score_overal)/len(score_overal)))

		# 	if score_genres.values().count(0.0) == len(score_genres.values()):
		# 		score_overall_genres = 0.0
		# 	else:
		# 		score_overall_genres = sum(score_genres.values())/(len(score_genres.values())-score_genres.values().count(0.0))
			
		# 	sf.write(';%1.2f;' % score_overall_genres)
		# 	for genre,score in score_genres.iteritems():
		# 		sf.write('|%s,%1.2f' % (genre,score))
		# 	sf.write('\n')

	def TEST_PEFORMANCE_train(self,movies_stars,movies):
		genres_code = dict([(g.split(';')[0],g.split(';')[1]) for g in open(PATH__GENRES_CODE).read().split('\n')])
		stars_data = {}
		for movie_star in movies_stars[:-1]:
			sp = movie_star.split(';')
			cast_movie = sp[1:]
			movie = sp[0]
			
			if movie not in movies:

				raise Exception('The movie %s is not in watched.movies. Remove from watched.cast' % movie)

			score = float(movies[movie][0])
			genres = movies[movie][1]
			
			for star in cast_movie:

				if star not in stars_data:
					
					stars_data[star] = {}
					for g in genres_code.values():
						stars_data[star][g] = []

				for g in genres:

					g = genres_code[g]
					stars_data[star][g].append(score)

			
		results_train = []
		for star, data_star in stars_data.iteritems():
			results_train.append([])
			if len(star) <= 1:
				continue
			scores = [d for d in data_star.values()]
			score_sum =  sum([sum(d) for d in data_star.values()])
			score_count = sum([len(d) for d in data_star.values()])
			score_overall = score_sum/float(score_count)
			
			
			results_train[-1].extend([star,score_overall,score_count])
			

			for code,key in genres_code.iteritems():
				if len(data_star[key]) == 0:
					results_train[-1].append(0)
				else:
					average_genre = sum(data_star[key])/float(len(data_star[key]))
					results_train[-1].append(average_genre)

		return results_train

	def TEST_PEFORMANCE_test(self,train_cast,test_cast,movies):

		result_test = []
		
		# train_cast = open(PATH__STAR_TRAIN_SCORE).read().split('\n')
		# train_cast = dict([(t.split(';')[0],t.split(';')[1:]) for t in train_cast])


		movies_stars = test_cast
		movies_cast = dict([(m.split(';')[0],m.split(';')[1:]) for m in movies_stars])
		genres_code = dict([(g.split(';')[0],g.split(';')[1]) for g in open(PATH__GENRES_CODE).read().split('\n')])
		
		
		# #This is a GAMBIARRA
		genres = dict([('Sci-Fi',-22),('Crime', -21), ('Romance', -20), ('Animation', -19), ('Music', -18), ('Comedy', -17), ('War', -16), ('Horror', -15), ('Adventure', -14), ('Thriller', -13), ('Western', -12), ('Mystery', -11), ('Short', -10), ('Drama', -9), ('Action', -8), ('Documentary', -7), ('Musical', -6), ('History', -5), ('Family', -4), ('Fantasy', -3), ('Sport', -2), ('Biography', -1)])
		
		t_cast = []
			
		for index in xrange(len(train_cast)):
			t = train_cast[index]
			if len(t) > 0:
				t_cast.append((t[0],t[1:]))
		train_cast = dict(t_cast)

		for title, cast in movies_cast.iteritems():
			# if title not in genres_movies:
			# 	print 'Title: "%s" movie has already watched. Remove register from new.cast' % title
			# 	wc = open(PATH__WATCHED_CAST,'a')
			# 	if len(title)>2:
			# 		wc.write('%s;%s\n' % (title,";".join(cast)))
			# 	wc.close()
			# 	continue

			name = movies[title][0]
			score_genres = {}
			score_overal = []

			for g in movies[title][1:][0]:
				
				if g not in genres and g != 'NA':
					raise Exception('%s:Genre %s does not exist' % (title,g))
				elif g != 'NA':
					cast_new_movie = movies_cast[title]
					score_genres[g] = []
					
					for star in cast_new_movie:

						if star in train_cast:
							
							score = float(train_cast[star][genres[g]])
							if score != 0:
								score_genres[g].append(float(score))
							score_overal.append(float(train_cast[star][0]))

					if len(score_genres[g]) == 0:
						score_genres[g] = 0
					else:
						score_genres[g] = sum(score_genres[g])/len(score_genres[g])
			
			result_test.append([])

			if len(score_overal) == 0:
				result_test[-1].extend([title,name,0])
			else:
				result_test[-1].extend([title,name,sum(score_overal)/len(score_overal)])

			if score_genres.values().count(0.0) == len(score_genres.values()):
				score_overall_genres = 0.0
			else:
				score_overall_genres = sum(score_genres.values())/(len(score_genres.values())-score_genres.values().count(0.0))
			result_test[-1].append(score_overall_genres)

			for genre,score in score_genres.iteritems():
				result_test[-1].extend([genre,score])

		return result_test

	def TEST_PEFORMANCE_score(self,test_results):
		
		target = []
		estimated = []
		variancia = []
		for t in test_results:
			if t[2] != 0:
				target.append(float(t[1]))
				estimated.append(t[2])
				variancia.append((t[2]-float(t[1]))**2)

		return cor(estimated,target),math.sqrt(sum(variancia)/len(variancia))

	def TEST_PEFORMANCE(self):
		movies_stars = open(PATH__WATCHED_CAST).read().split('\n')[:-1]
		movies_data = open(PATH__WATCHED_MOVIES).read().split('\n')
		movies = dict([(m.split(';')[0],[m.split(';')[1],m.split(';')[2:]]) for m in movies_data])
		

		data_cv = crossValidation(list(movies_stars))
		

		##TRAIN
		cor_geral = 0
		desvio_geral = 0
		for sample in data_cv:
				train_cv = TEST_PEFORMANCE_train(sample['Train'],movies)
				test_cv = TEST_PEFORMANCE_test(train_cv,sample['Test'],movies)
				results = TEST_PEFORMANCE_score(test_cv)
				cor_geral += results[0]
				desvio_geral += results[1]
		print cor_geral/4,desvio_geral/4

	def run(self):
		print 'Running Cast'
		#crawly_cast()
		#train_cast()
		self.test_cast()
	#TEST_PEFORMANCE()


if "__main__":
	c = Cast()
	c.run()
