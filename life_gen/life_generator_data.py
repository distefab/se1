import pandas as pd
import subprocess as sp
from os import path
from life_generator_debug import log


class PopulationData:
    def __init__(self):
        current_dir = path.dirname(path.realpath(__file__))
        parent_dir = path.dirname(current_dir)
        population_dir = path.join(parent_dir, "population-generator")
        self.program_path = path.join(population_dir, "population-generator.py")
        self.input_file = path.join(population_dir, "input.csv")
        self.output_file = path.join(population_dir, "output.csv")
        self.command = "python"

    def _run_command(self):
        args = [self.command, self.program_path, self.input_file]
        log(f"Running: {args}")
        sp.run(args)

    def _get_output_as_df(self):
        df = pd.read_csv(self.output_file)
        return df

    def _get_data(self):
        self._run_command()
        self.df = self._get_output_as_df()

    def get_data_as_string(self, completion):
        self._get_data()
        result = self.df.at[0, "output_population_size"]
        completion(result)


class ToyData:
    def __init__(self):
        dir = path.dirname(path.realpath(__file__))
        self.data_filepath = path.join(dir, "amazon_co-ecommerce_sample.csv")
        self.output_filepath = path.join(dir, "output.csv")

    def load(self):
        df = pd.read_csv(self.data_filepath)

        # add
        df["input_item_type"] = "toys"
        df["input_number_to_generate"] = None

        # map
        df["input_item_category"] = df.amazon_category_and_sub_category.apply(
            lambda s: str(s).split(">", 1)[0].strip()
        )

        # rename
        df = df.rename(
            columns={
                "uniq_id": "id",
                "product_name": "output_item_name",
                "average_review_rating": "output_item_rating",
                "number_of_reviews": "output_item_num_reviews",
            }
        )

        # prune
        columns = [
            "id",
            "input_item_type",
            "input_item_category",
            "input_number_to_generate",
            "output_item_name",
            "output_item_rating",
            "output_item_num_reviews",
        ]
        df = df[columns]

        # store
        self.df = df

    def categories(self):
        categories = self.df.input_item_category.unique()

        # clean
        cleaned = [cat for cat in categories if cat.lower() != "nan"]

        return sorted(cleaned)

    def calc_top_toys_for(self, categories, completion):

        result = pd.DataFrame(columns=self.df.columns)

        log("Calculating top toys for categories:", categories)
        for category, count in categories:
            # 1. Sort category Y by uniq_id (0 to 9, A to Z), then by number_of_reviews (most to least)
            items = self.df.loc[self.df["input_item_category"] == category]
            items = items.sort_values(
                ["output_item_num_reviews", "id"],
                ascending=[False, True],
            )
            log("Items: ", items)

            # 2. Take the top X*10
            items = items.head(count * 10)

            # 3. Sort those by uniq_id (0 to 9, A to Z), then by average_review_rating (highest to lowest)
            items = items.sort_values(
                ["output_item_rating", "id"],
                ascending=[False, True],
            )
            log("Head: ", items)

            # 4. Take the top X
            items = items.head(count)

            items["input_number_to_generate"] = count
            log("Final: ", items)
            result = result.append(items)

        completion(result)

    # Expected input format:
    #   input_item_type,input_item_category,input_number_to_generate
    def calc_top_toys_from_file(self, filepath, completion):
        input = pd.read_csv(filepath)

        # filter for toys
        input = input[input["input_item_type"] == "toys"].drop(
            columns=["input_item_type"]
        )
        # convert to tuples
        categories = [tuple(row) for row in input.values]
        # get results
        self.calc_top_toys_for(categories, completion)

    # Output format:
    #   input_item_type,input_item_category,input_number_to_generate,output_item_name,
    #     output_item_rating,output_item_num_reviews
    def export(self, df):
        path = self.output_filepath
        output = df.drop(columns=["id"])
        output.to_csv(path, index=False)
        log(f"Exported to: {path}")

    def set_output_filepath(self, filepath):
        self.output_filepath = filepath


def user_confirm_action(prompt):
    response = None
    first_time = True
    while response != "y" and response != "n":
        if not first_time:
            print("Invalid input.")
        first_time = False
        response = input(prompt + "(y/n): ")

    return response == "y"
