# User Study
- Target Group: Master Students of Business Informatics & Computer Science
- No. of respondents: ~10
- Platform: LimeSurvey (self-hosted)

## Page 0: Survey Start
Welcome to this anonymous user study on a novel algorithm for Explainable AI.
We do not expect you to have any prior knowledge on the topic - you will be provided with all the information you need to complete the survey. Please expect it to take around 10-15 minutes of your time.

## Page 1: Demographic Data
We will begin by asking you a few questions about yourself. You may always choose the "No answer" option in case you do not want to tell. This study is open to anyone, independent of the answers you provide here.

_Q: Please indicate the level of educational or professional experience you have in the fields of general computer science or Artificial Intelligence (AI) (None, some experience, high experience, prefer not to tell)_

_Q: Please indicate the highest academic degree that you either have completed or are currently pursuing (any field, not limited to computer science or AI) (Bachelor/Undergraduate, Master/Graduate, PhD, None of these, prefer not to tell)_

_Q: Please indicate the gender you identify with (female, male, non-binary, prefer not to tell)_

_Q: Please indicate your age (18-24, 25-34, 35-44, 45-54, 55-64, 65 and over, prefer not to tell)_

Thank you! Let's start with the core study.


## Page 1: Introduction to Data Mining
Data mining is “the discovery of interesting, unexpected, or valuable structures in large datasets” [1, p. 621]. One specific task in data mining is classification, where an algorithm (classifier) is tasked to guess the correct group (class) for each entry in a set of entities. An example could be a classifier that predicts whether a movie is going to be rated as good or bad, given some information about the movie itself.

[illustration of movie classifier]

_Q: Before taking this survey, were you already familiar with those basic facts about data mining and the classification task (Yes/No/No answer)?_

[1] D. J. Hand, “Principles of Data Mining,” Drug Safety, vol. 30, no. 7, pp. 621–622, 2007.

## Page 2: Introduction to Knowledge Graphs
For this study, we have trained an actual classifier for the movie example given above. It uses information that comes from _DBpedia_, a popular knowledge graph based on semi-structured information found in Wikipedia entries. Although there are several opinions on how to define a knowledge graph, one can describe it loosely as “graph of data intended to accumulate and convey knowledge of the real world, whose nodes represent entities of interest and whose edges represent relations between these entities” [2, p.2]. Below we depict a sample illustration of what could be a small part of a knowledge graph. 

[sample illustration knowledge graph]

_Q: Before taking this survey, were you already familiar with those basic facts about knowledge graphs (Yes/No/No answer)?_

[2] A. Hogan et al., “Knowledge Graphs,” ACM Comput. Surv., vol. 54, no. 4, pp. 1–37, 2022.

## Page 3: Trust in Movie Classifier 
Our classifier is tasked to predict whether a movie will receive a good rating on Metacritic, an online platform that aggregates reviews from multiple sources.

Example: [Movie, Genre, Year, Director] is predicted to be rated as [good]. 

In the following, you will see 10 other predictions made by the classifier.
At the time of training, the classifier achieved an accuracy of xx% on previously unseen training data.

_Q: Without looking up the actual movie rating, please indicate for each prediction how much you trust it to be accurate (0 - not at all; 5 - full trust)._

[... 10 examples, Movie, Genre, Year, Director, Prediction ...]

_Q: After having evaluated 10 prediction examples, how much do you trust the classifier to make accurate predictions for future movies (0 - not at all; 5 - full trust)?_

## Page 4: Trust in Movie Classifier with Explanations
We will now again show you the predictions of the movie classifier, this time with a visualization of facts in the knowledge graph. We will highlight facts that the classifier considers to be important for the rating.

As an example, the explanation provided for the prediction
- [example from above]

is seen here:
- [explanation]

Green edges indicate that the classifier considers a relationship to have a positive impact on movie rating, while red edges indicate a presumed negative impact. The stroke size of a relation indicates how strong this effect is considered to be. Blue edges do not have a large impact on the prediction. The relationship with the strongest absolute impact is additionally labeled with a weight of 1.0, the other relationships receive a label relative to this maximum (linear gradient). 

_Q: Without looking up the actual movie rating, please indicate how much you trust the respective prediction to be accurate (0 - not at all; 5 - full trust). Please additionally indicate how helpful the explanations are in evaluating the classifier (0 - not at all; 5 - very helpful)._

[... 10 same examples with explanations ...]

_Q: After having evaluated 10 prediction examples combined with explanations, how much do you trust the classifier to make accurate predictions for future movies (0 - not at all; 5 - full trust)?_

## Page 5: Trust in Album Classifier
We will repeat the experiment with a different classifier. 

[...] 
## Page 6: Trust in Album Classifier with Explanations 
[...] 

## Page 7: Overall Usefulness of Explanations

Now that you have worked with our graph explanations for some time, we would like to evaluate their overall usefulness.

_Q: Please indicate if the graph explanations were easy to understand (0 - very complex; 5 - easy to understand)._

_Q: Please indicate if you found the graph explanations to be helpful in evaluating the classifiers (0 - not at all; 5 - very helpful)._

_Q: Please indicate how likely it is that you would recommend the usage of such a graph-based explanation and visualization approach to a friend or colleague with a similar use case (Net Promoter Score: 0 - unlikely; 10 - very likely)._

_Q: In case you would like to provide any written feedback to the explanations, please do so here: (free text)_

_Q: In case you would like to provide overall feedback to this survey, please do so here: (free text)_

## Page 8: Survey End
Thank you for your participation!

If you would like to learn more about the explanation method you just evaluated, feel free to message me at (1)@(2).de. You are also most welcome to read my thesis once it is finished.

(1): rgrenz
(2): mail.uni-mannheim

Have a fantastic day!
- Rouven

---
SVG?