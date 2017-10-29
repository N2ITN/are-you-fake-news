   @timeit
    def plot(self):

        results_ = {k: v for k, v in self.results.items() if v != 0}
        y, x = list(zip(*sorted(results_.items(), key=lambda kv: kv[1], reverse=True)))

        x = x / np.sum(x)
        sns.set()

        def label_cleaner():
            key = {
                'fakenews': 'fake news',
                'extremeright': 'extreme right',
                'extremeleft': 'extreme left',
                'veryhigh': 'very high veracity',
                'low': 'low veracity',
                'pro-science': 'pro science',
                'mixed': 'mixed veracity',
                'high': 'high veracity'
            }
            for label in y:
                for k, v in key.items():
                    if label == k:
                        label = v.title()

                yield label.title()

        y = list(label_cleaner())

        y_pos = np.arange(len(y))
        plt.figure(figsize=(8, 8))
        sns.barplot(y=y_pos, x=x, palette='viridis_r', orient='h')
        plt.yticks(y_pos, y)
        plt.ylabel('Usage')
        plt.title(self.url.replace('https://', '').replace('http://', ''))

        name = ''.join([
            c for c in self.url.replace('https://', '').replace('http://', '').replace('www.', '')
            if c.isalpha()
        ])
        plt.savefig('static/{}.png'.format(name), format='png', bbox_inches='tight', dpi=300)
        plt.show()


class CombineResults:

    def __init__(self):
        self.pol = [
            'extremeright', 'right-center', 'right', 'center', 'left-center', 'left', 'extremeleft'
        ]
        self.cred = ['fakenews', 'low', 'unreliable', 'mixed', 'high', 'veryhigh']
        self.results = addDict({})

    def __add__(self, new_article):

        print(self.results)
        self.results = self.results + addDict(new_article[0])

    def __iadd__(self, new_article):
        return self.results + addDict(new_article[0])

    def softmax(self):
        # self.results = self.lickert_scale()
        self.results = self.argmax()
        return self.results

    def argmax(self):
        pol = self.pol
        cred = self.cred
        cred_max = self.results.argmax(cred, n=1)
        pol_max = self.results.argmax(pol, n=1)
        for k in pol + cred:
            self.results[k] = 0.

        self.results[pol_max[0][0]] = pol_max[0][1]
        self.results[cred_max[0][0]] = cred_max[0][1]
        return self.results

    def lickert_scale(goal):
        weights = []
        scores = []
        for i, k in enumerate(goal, start=1):
            if k in self.results:
                weights.append(i * self.results[k])
                scores.append(self.results[k])
        ave = np.mean(weights)
        best = goal[int(round(ave / np.sum(scores)))]

        for k in goal:
            if k != best:
                self.results[k] = 0.0001

        return self.results