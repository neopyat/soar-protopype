from analyzers.bruteforce import BruteForceAnalyzer


def get_analyzers(config=None):
    analyzers = []

    # базовые правила
    analyzers.append(BruteForceAnalyzer(threshold=5))

    # сюда потом подключим ML
    if config and config.get("use_ml"):
        pass

    return analyzers