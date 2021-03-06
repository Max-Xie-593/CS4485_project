import pandas as pd
from typing import List, Text, Tuple
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import CountVectorizer
# from bace.classifiers.classifier import Classifier
from os.path import join as path_join
import argparse

def read_data(filename: Text) -> Tuple[List[Text], List[Text]]:
    dataset = pd.read_csv(filename)
    return dataset['filename'].tolist(),\
           dataset['label'].tolist(), \
           dataset['tokens'].tolist()


def get_classifier(train_labels: List[Text], train_data: List[Text], num_features: int = 200):
    classifier = GaussianNB()
    classifier.fit(CountVectorizer(max_features = num_features).fit_transform(train_data).toarray(),train_labels)
    return classifier


def predict(classifier: GaussianNB, test_data:List[Text], num: int = 200):
    return classifier.predict(CountVectorizer(max_features = num).fit_transform(test_data).toarray())


def show_metrics(test_labels: List[Text], class_prediction: List[Text]):
    print(confusion_matrix(test_labels,class_prediction))
    print(classification_report(test_labels,class_prediction))
    print("Accuracy:", accuracy_score(test_labels,class_prediction))



def run_bagofwords(args):
    train_fnames, train_labels, train_tokens = read_data(args.training_file)
    test_fnames, test_labels, test_tokens = read_data(args.test_file)

    clf = get_classifier(train_labels, train_tokens, args.num_features)

    predictions = predict(clf, test_tokens, num=args.num_features)

    if args.metrics:
        show_metrics(test_labels, predictions)
    else:
        for i in range(len(predictions)):
            print(test_fnames[i],
                  test_labels[i],
                  predictions[i],
                  test_labels[i] == predictions[i]
                  #train_tokens[i]
                  )

def construct_parser_bow(subparser):
    """
    if subparser:
        bow_parser = subparser.add_parser(
            "bow",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            help="Bag of words Classifier"
        )
    else:
        bow_parser = argparse.ArgumentParser(
            description='Bag of words Classifier',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
    """
    #subparser.set_defaults(description="BAG OF WORDS ASDJFAHEKJD")

    subparser.add_argument(
        'training_file', type=str, default="data_clean", metavar="input-dir",
        help='Path to training .csv'
    )
    subparser.add_argument(
        '-o', '--output_dir', type=str, default="results",
        help='Output directory to hold bow classifier output files'
    )
    subparser.add_argument(
        '-t', '--test_file', type=str, default="test_texts.csv",
        help='Path to test .csv or .csv to predict'
    )
    subparser.add_argument(
        '-n', '--num_features', type=int, default=200,
        help='number of features to use in bag of words classification'
    )

    # Make results showing options mutually exclusive
    subparser.add_argument(
        '-m', '--metrics', action="store_true", default=False,
        help="Flag to just show metrics instead of predictions"
    )

    subparser.add_argument(
        '-s', '--slice', type=int, metavar="i",
        help="Flag to label slices of the ith document in the test .csv"
    )

    subparser.set_defaults(run=run_bagofwords)

    # if we choose whole documents
        # for each doc
            # print :
                # fileName [most probable class : probability, second most probable class : probability...]
    # if we choose one doc, sliced
        # for each slice
            # print
                # predict label : the slice
