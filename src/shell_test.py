__author__ = 'E440'



def gender_features(name):
      features = {}
      for letter in 'abcdefghijklmnopqrstuvwxyz':
        features['count(%s)' % letter] = name.lower().count(letter)
        features['has(%s)' % letter] = letter in name.lower()
        features['startswith(%s)' % letter] = (letter==name[0].lower())
        features['endswith(%s)' % letter] = (letter==name[-1].lower())
      return features

if __name__ == "__main__":

    import nltk as nltk
    from nltk.corpus import names
    import random
    names = ([(name, 'male') for name in names.words('male.txt')] +[(name, 'female') for name in names.words('female.txt')])
    random.shuffle(names)
    featuresets = [(gender_features(n), g) for (n,g) in names]
    train_set, test_set = featuresets[500:], featuresets[:500]
    classifier =nltk.WekaClassifier.train(r'c:/name.model',train_set,'weka.classifiers.functions.Logistic')
    print(nltk.classify.accuracy(classifier, test_set))
    ls = ["Alex","Neo","vivian","tom"]
    result = classifier.batch_classify([gender_features(name) for name in ls])
    print(result)