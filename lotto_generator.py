import argparse
import random


def generate_lotto_numbers(count=6, minimum=1, maximum=45):
    if count > maximum - minimum + 1:
        raise ValueError("count cannot be larger than the number range")

    return sorted(random.sample(range(minimum, maximum + 1), count))


def main():
    parser = argparse.ArgumentParser(description="Lotto number generator")
    parser.add_argument(
        "-g",
        "--games",
        type=int,
        default=5,
        help="number of lotto games to generate (default: 5)",
    )
    args = parser.parse_args()

    if args.games < 1:
        raise SystemExit("games must be at least 1")

    for index in range(1, args.games + 1):
        numbers = generate_lotto_numbers()
        print(f"Game {index}: {' '.join(f'{number:02d}' for number in numbers)}")


if __name__ == "__main__":
    main()
