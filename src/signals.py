import numpy as np


CLASS_NAMES = {
    0: "SELL",
    1: "HOLD",
    2: "BUY"
}


def return_to_signal(predicted_return, threshold=0.005):
    """
    Convert a predicted return into a Buy/Hold/Sell signal.

    Parameters
    ----------
    predicted_return : float
        Predicted stock return.

    threshold : float
        Decision threshold. Default 0.005 means 0.5%.

    Returns
    -------
    str
        SELL, HOLD, or BUY.
    """
    if predicted_return < -threshold:
        return "SELL"
    elif predicted_return > threshold:
        return "BUY"
    else:
        return "HOLD"


def class_to_signal(class_id):
    """
    Convert a numerical class label into a readable signal.

    Expected classes:
    0 = SELL
    1 = HOLD
    2 = BUY
    """
    return CLASS_NAMES.get(int(class_id), "UNKNOWN")


def probabilities_to_signal(probabilities):
    """
    Convert model class probabilities into a final Buy/Hold/Sell signal.

    Expected probability order:
    [SELL, HOLD, BUY]

    Parameters
    ----------
    probabilities : array-like
        Array containing probabilities for SELL, HOLD, and BUY.

    Returns
    -------
    dict
        Dictionary with class probabilities and final signal.
    """
    probabilities = np.array(probabilities).flatten()

    if len(probabilities) != 3:
        raise ValueError("Expected exactly 3 probabilities: [SELL, HOLD, BUY].")

    predicted_class = int(np.argmax(probabilities))

    return {
        "sell_probability": float(probabilities[0]),
        "hold_probability": float(probabilities[1]),
        "buy_probability": float(probabilities[2]),
        "predicted_class": predicted_class,
        "final_signal": class_to_signal(predicted_class)
    }


def format_signal_output(signal_result):
    """
    Format signal result into readable text for the final demo notebook.
    """
    return (
        f"SELL probability: {signal_result['sell_probability']:.2%}\n"
        f"HOLD probability: {signal_result['hold_probability']:.2%}\n"
        f"BUY probability: {signal_result['buy_probability']:.2%}\n"
        f"Final prototype signal: {signal_result['final_signal']}"
    )
