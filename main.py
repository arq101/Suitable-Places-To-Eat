import argparse
import pandas as pd
from pathlib import Path
from typing import Dict, Optional
import json


def arg_parser() -> argparse.Namespace:
    """Process command line arguments
    """
    parser = argparse.ArgumentParser(description='finds safe places to eat for team members')
    parser.add_argument('-o', '--output', help='Output json file path', default='./result_places_to_go.json')
    required_arg = parser.add_argument_group('Required named arguments')
    required_arg.add_argument('-u', '--users', dest='users', required=True,
                              help='path to json file defining team members food & drink requirements')
    required_arg.add_argument('-v', '--venues', dest='venues', required=True,
                              help="path to json file outlining food & drink options")
    return parser.parse_args()


def load_dataframe(src_file: Path) -> pd.DataFrame:
    """Creates dataframe from given source file
    """
    if Path(src_file).suffix.lower() == '.json':
        df = pd.read_json(src_file)
        return df
    raise ValueError(f'Unexpected file type: {src_file}')


def find_places_good_to_eat(users: pd.DataFrame, venues: pd.DataFrame) -> pd.DataFrame:
    """Returns dataframe defining places safe to eat for each user
    """
    good_places_df = pd.DataFrame(columns=['venue', 'safe_to_eat_for'])
    for idx, row in venues.iterrows():
        venue_name = row['name']
        venue_foods = row['food']
        temp_users_df = users[~users['wont_eat'].apply(lambda x: bool(set(x) & set(venue_foods)))]
        suitable_users = temp_users_df['name'].to_list()
        good_places_df = good_places_df.append(
            {'venue': venue_name, 'safe_to_eat_for': suitable_users}, ignore_index=True
        )
    return good_places_df


def places_to_visit(mapped_places: pd.DataFrame, users: pd.DataFrame) -> Dict:
    """Lists places safe to eat for the whole team.
    """
    number_of_users = len(users)
    df = mapped_places[mapped_places['safe_to_eat_for'].apply(lambda x: len(x) == number_of_users)]
    return dict(places_to_visit=df['venue'].to_list())


def places_to_avoid():
    # TODO
    pass


def produce_json_output(places_data: Dict, file_path: Optional[str]) -> None:
    """Prints the json output and produces optional output json file
    """
    json_obj = json.dumps(places_data, indent=4)
    print(json_obj)

    if file_path:
        with open(file_path, 'w') as fh:
            json.dump(places_data, fh)
    return


def main():
    cmdline_args = arg_parser()
    users_df = load_dataframe(cmdline_args.users)
    venues_df = load_dataframe(cmdline_args.venues)

    suitable_places_for_user = find_places_good_to_eat(users=users_df, venues=venues_df)
    safe_to_go_for_team = places_to_visit(mapped_places=suitable_places_for_user, users=users_df)
    produce_json_output(places_data=safe_to_go_for_team, file_path=cmdline_args.output)


if __name__ == '__main__':
    main()
