import data_infra

# File which provides data reading and streaming capabilities
INITIAL_TRAIN_SIZE=0.2

class DataSet(object):

    def __init__(self, filename, initial_train_size=INITIAL_TRAIN_SIZE):
        [X,Y]=data_infra.ReadFromFile(filename)
        [X_train, Y_train, X_test, Y_test]=data_infra.SplitTrainAndTest(X,Y, initial_train_size)
        self.train_set= {'X': X_train, 'Y': Y_train}
        self.test_set= {'X': X_test, 'Y': Y_test}
        self.data_describe={
            'name': filename,
            'size': len(Y),
            'dimensionality': len(X[0]),
            'train_size': len(Y_train),
            'test_size': len(Y_test)
        }

    def describeDataset(self):
        return self.data_describe

    def printDataDescription(self):
        print 'Description of Dataset'
        for key, value in self.data_describe.items():
            print key, value

class Oracle(object):
    def __init__(self,Y):
        self.ground_truth=Y
        self.expenditure=0

    def getTrueLabelEvaluation(self,id):
        return self.ground_truth[id]

    def getTrueLabel(self,id, cost=1):
        expenditure+=cost
        return self.ground_truth[id]

class Stream(object):

    def __init__(self, X, Y, chunk_size=1, slide_rate=None):
        if slide_rate is None:
            slide_rate=chunk_size
        self.size=len(Y)
        self.unlabaled_data=X
        self.true_labels=Y
        self.chunk_size=chunk_size
        self.slide_rate=slide_rate

        self.current_timestamp=-self.chunk_size
        self.current_chunk=None
        self.is_stream_end=False
        self.evaluated_intervals=0

        self.got_chunk_before_evalaution=False

    def _getNextChunk(self):
        start_timestamp=self.current_timestamp+self.slide_rate
        end_timestamp=start_timestamp+chunk_size
        if self.end_timestamp> self.size:
            self.end_timestamp=self.size
            self.is_stream_end=True
        self.current_chunk= \
            { 'X': self.unlabaled_data[start_timestamp:end_timestamp],
              'Y': self.true_labels[start_timestamp:end_timestamp]}
        self.current_timestamp=start_timestamp
        self.evaluated_intervals+=1
        self.got_chunk_before_evalaution=False

    def getUnlabaledData(self):
        self._getNextChunk()
        self.got_chunk_before_evalaution=True
        return self.current_chunk['X']

    def getEvaluationLabels(self):
        if  self.got_chunk_before_evalaution:
            return self.current_chunk['Y']
        else:
            raise Exception('Did not fetch before accessing labels')







