from typing import Any

from opik.evaluation.metrics import base_metric, score_result

from news_sentiment.baml_client.types import SentimentScore


class SameScoreMetric(base_metric.BaseMetric):
    def __init__(
        self,
        name: str,
        coin: str,
    ):
        self.name = name
        self.coin = coin

    def _has_non_zero_score(self, scores: list[dict[str, int]]) -> bool:
        """
        Returns True if `scores` list has a non-zero element for the coin `self.coin`
        False otherwise.
        """
        return any(x['coin'] == self.coin and x['score'] != 0 for x in scores)

    def _get_score(self, scores: list[dict[str, int]]) -> int:
        """
        Returns the score for the coin `self.coin`
        """
        return [x for x in scores if x['coin'] == self.coin][0]['score']

    def score(
        self,
        input: str,
        scores: list[SentimentScore],
        expected_output: list[dict[str, int]],
        **ignored_kwargs: Any,
    ):
        # transform `scores` as a list of dictionaries
        scores = [{'coin': str(x.coin), 'score': x.score} for x in scores]

        # The only way the `value` is 1 if if:
        # 1. `scores` and `expected_output` are both empty
        # 2. `scores` and `expected_output` have a non-zero score for the coin `self.coin`
        #    and the score is the same.
        value = 0
        if (not self._has_non_zero_score(scores)) and (
            not self._has_non_zero_score(expected_output)
        ):
            value = 1

        elif self._has_non_zero_score(scores) and self._has_non_zero_score(
            expected_output
        ):
            # both `scores` and `expected_output` have a non-zero score for the coin `self.coin`
            # If that score is the same, then the value is 1, otherwise 0.
            value = (
                1 if self._get_score(scores) == self._get_score(expected_output) else 0
            )

        # Add you logic here
        # TODO: Implement the logic to score the sentiment extractor
        return score_result.ScoreResult(
            value=value,
            name=self.name,
            # reason='Optional reason for the score'
        )
