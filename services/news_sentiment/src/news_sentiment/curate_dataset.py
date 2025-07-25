import json

from opik import Opik


def mark_item_as_correct(dataset, item):
    """
    Marks the item as correct in the dataset by adding a new column called `is_human_verified`
    and setting it to True
    """
    # opik has no method to update a row, so we need to delete the row and add it back
    # with the new information
    # breakpoint()
    dataset.delete(items_ids=[item['id']])
    new_item = {
        **item,
        'is_human_verified': True,
    }
    # breakpoint()
    dataset.insert([new_item])


def ask_human_for_correction(dataset, item):
    """
    Asks the human for a correction of the item's field:
    - expected_output (which needs to be valid list of JSON)
    - expected_reason (which needs to be a valid string saying why the items' scores are what they are)
    """
    # Ask the user to provide the `expected_output` and validate it is a valid list of JSON
    while True:
        expected_output = input('Please provide the expected output (a list of JSON): ')
        try:
            expected_output = json.loads(expected_output)
            break
        except json.JSONDecodeError:
            print('Invalid JSON, please try again')
            continue

    # Ask the user to provide the `expected_reason` and validate it is a valid string
    while True:
        expected_reason = input('Please provide the expected reason: ')
        if expected_reason:
            break
        else:
            print('Invalid reason, please try again')
            continue

    # Update the item with the new information
    item['expected_output'] = expected_output
    item['expected_reason'] = expected_reason

    mark_item_as_correct(dataset, item)


def curate_dataset(dataset_name: str):
    """
    Curates the dataset with a human in the loop.
    """
    # Load the dataset we want to curate
    print(f'Curating dataset: {dataset_name}')
    client = Opik()
    dataset = client.get_or_create_dataset(name=dataset_name)

    # Load the dataset items that are not human verified
    dataset_items = json.loads(dataset.to_json())
    dataset_items = [
        item for item in dataset_items if not item.get('is_human_verified', False)
    ]
    print(
        f'Loaded {len(dataset_items)} items from the dataset that are not human verified'
    )

    for item in dataset_items:
        print('--------------------------------')
        print('input: ', item['input'])
        print('--------------------------------')
        print('expected_output: ', item['expected_output'])
        print('--------------------------------')
        print('expected_reason: ', item['expected_reason'])
        print('--------------------------------')
        print('teacher_model: ', item['teacher_model'])
        print('--------------------------------')

        # Ask the user whether the item is correct or not
        while True:
            is_correct = input('Is the item correct? (y/n): ')
            if is_correct == 'y':
                mark_item_as_correct(dataset, item)
                break
            elif is_correct == 'n':
                ask_human_for_correction(dataset, item)
                break
            else:
                print('Invalid input')
                continue


if __name__ == '__main__':
    from fire import Fire

    Fire(curate_dataset)
