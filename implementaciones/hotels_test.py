from main_hotels import get_values


def main(file, json_name):
    get_values(file, json_name)


if __name__ == '__main__':
    main("../csv_files/test.csv", "test")
