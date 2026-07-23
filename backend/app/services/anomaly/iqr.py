import numpy as np

Number = int | float


class IQRDetector:
    """Interquartile Range (IQR) based anomaly detector."""

    @staticmethod
    def detect(
        values: list[Number],
        multiplier: float = 1.5,
    ) -> list[bool]:
        """
        Detect anomalies using the IQR method.

        Args:
            values: List of numeric values.
            multiplier: IQR multiplier.

        Returns:
            List of boolean values where True indicates an anomaly.
        """

        if not values:
            return []

        data = np.array(values, dtype=float)

        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)

        iqr = q3 - q1

        lower_bound = q1 - (multiplier * iqr)
        upper_bound = q3 + (multiplier * iqr)

        return [
            bool(value < lower_bound or value > upper_bound)
            for value in data
        ]


if __name__ == "__main__":
    sample_data: list[Number] = [
        10,
        12,
        13,
        14,
        15,
        16,
        18,
        20,
        22,
        200,
    ]

    anomalies = IQRDetector.detect(sample_data)

    print("Values     :", sample_data)
    print("Anomalies  :", anomalies)