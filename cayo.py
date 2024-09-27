def plan_loot_distribution(loot_info, players, is_hard_mode):
    """
    Plan the most efficient loot bag mix for each player in the GTA V Online Cayo Perico Heist,
    accounting for the number of clicks per loot stash stack.

    Args:
        loot_info (dict): A dictionary containing the available loot quantities and primary target.
                          Example:
                          {
                              'primary_target': {'name': 'Sinsimito Tequila'},
                              'gold': 2,
                              'cocaine': 2,
                              'weed': 2,
                              'painting': 1,
                              'cash': 4
                          }
        players (int): Number of players participating in the heist.
        is_hard_mode (bool): True if the heist is in hard mode, False otherwise.

    Returns:
        dict: A dictionary containing each player's loot mix, total value, and total bag space used.
    """
    # Define loot types and attributes
    LOOT_TYPES = {
        'gold': {
            'value_per_stack': 328_584,
            'bag_space_per_stack': 66.67,
            'clicks_per_stack': 10
        },
        'cocaine': {
            'value_per_stack': 220_500,
            'bag_space_per_stack': 50.0,
            'clicks_per_stack': 10
        },
        'weed': {
            'value_per_stack': 145_980,
            'bag_space_per_stack': 37.5,
            'clicks_per_stack': 10
        },
        'painting': {
            'value_per_stack': 176_200,
            'bag_space_per_stack': 50.0,
            'clicks_per_stack': 1  # Paintings are collected in one action
        },
        'cash': {
            'value_per_stack': 78_480,
            'bag_space_per_stack': 25.0,
            'clicks_per_stack': 10
        }
    }

    # Define primary targets and their values
    PRIMARY_TARGETS = {
        'Sinsimito Tequila': {
            'normal': 630_000,
            'hard': 693_000
        },
        'Ruby Necklace': {
            'normal': 700_000,
            'hard': 770_000
        },
        'Bearer Bonds': {
            'normal': 770_000,
            'hard': 847_000
        },
        'Pink Diamond': {
            'normal': 1300_000,
            'hard': 1430_000
        },
        'Panther Statue': {
            'normal': 1900_000,
            'hard': 2090_000
        }
    }

    # Compute value and bag space per click for each loot type
    for loot_type in LOOT_TYPES:
        loot_data = LOOT_TYPES[loot_type]
        loot_data['value_per_click'] = loot_data['value_per_stack'] / loot_data['clicks_per_stack']
        loot_data['bag_space_per_click'] = loot_data['bag_space_per_stack'] / loot_data['clicks_per_stack']
        # Value per 1% bag space
        loot_data['value_per_1_percent'] = loot_data['value_per_click'] / loot_data['bag_space_per_click']

    # Create a priority list of loot types based on value per 1% bag space
    loot_priority = sorted(
        LOOT_TYPES.items(),
        key=lambda x: x[1]['value_per_1_percent'],
        reverse=True
    )

    # Initialize players' bag capacities and loot
    player_bags = []
    for _ in range(players):
        player_bags.append({
            'capacity': 100.0,  # Each player's bag can hold 100%
            'loot': {}
        })

    # Initialize loot stacks for each loot type
    loot_stacks = {}
    stack_id_counter = 0  # To uniquely identify each stack
    for loot_type in LOOT_TYPES:
        quantity = loot_info.get(loot_type, 0)
        stacks = []
        for _ in range(quantity):
            stacks.append({
                'stack_id': stack_id_counter,
                'remaining_clicks': LOOT_TYPES[loot_type]['clicks_per_stack']
            })
            stack_id_counter += 1
        loot_stacks[loot_type] = stacks

    # Distribute loot among players based on priority
    for loot_type, loot_data in loot_priority:
        stacks = loot_stacks.get(loot_type, [])
        if not stacks:
            continue  # Skip if no stacks of this loot type are available

        for stack in stacks:
            while stack['remaining_clicks'] > 0:
                loot_assigned = False
                for player in player_bags:
                    if player['capacity'] <= 0:
                        continue  # Skip if the player's bag is full

                    # Calculate the maximum number of clicks the player can take from this stack
                    max_clicks_player_can_take = int(player['capacity'] // loot_data['bag_space_per_click'])
                    clicks_to_take = min(max_clicks_player_can_take, stack['remaining_clicks'])

                    if clicks_to_take <= 0:
                        continue  # Player can't take more loot

                    # Update player's capacity and loot
                    bag_space_used = clicks_to_take * loot_data['bag_space_per_click']
                    value_collected = clicks_to_take * loot_data['value_per_click']
                    player['capacity'] -= bag_space_used

                    # Initialize loot entry if not present
                    if loot_type not in player['loot']:
                        player['loot'][loot_type] = {
                            'stacks': []
                        }

                    # Add loot details
                    player['loot'][loot_type]['stacks'].append({
                        'stack_id': stack['stack_id'],
                        'clicks': clicks_to_take,
                        'bag_space_used': bag_space_used,
                        'value': value_collected
                    })

                    # Update the stack's remaining clicks
                    stack['remaining_clicks'] -= clicks_to_take

                    loot_assigned = True

                    # Break if the player's bag is full or the stack is depleted
                    if player['capacity'] <= 0 or stack['remaining_clicks'] <= 0:
                        break

                if not loot_assigned:
                    break  # No player can take more from this stack

    # Prepare the result dictionary
    result = {}
    for idx, player in enumerate(player_bags):
        player_loot = {}
        total_value = 0
        total_bag_space_used = 0

        for loot_type, loot_info in player['loot'].items():
            loot_data = LOOT_TYPES[loot_type]
            total_clicks = sum(stack['clicks'] for stack in loot_info['stacks'])
            total_value_loot = sum(stack['value'] for stack in loot_info['stacks'])
            total_bag_space_loot = sum(stack['bag_space_used'] for stack in loot_info['stacks'])

            player_loot[loot_type] = {
                'total_clicks': total_clicks,
                'stacks': [
                    {
                        'stack_id': stack['stack_id'],
                        'clicks': stack['clicks'],
                        'bag_space_used': round(stack['bag_space_used'], 2),
                        'value': int(stack['value'])
                    }
                    for stack in loot_info['stacks']
                ],
                'total_value': int(total_value_loot),
                'total_bag_space_used': round(total_bag_space_loot, 2)
            }

            total_value += total_value_loot
            total_bag_space_used += total_bag_space_loot

        result[f'Player {idx + 1}'] = {
            'loot': player_loot,
            'total_value': int(total_value),
            'total_bag_space_used': round(100.0 - player['capacity'], 2)
        }

    # Add primary target information
    primary_target_info = loot_info.get('primary_target', {})
    primary_target_name = primary_target_info.get('name', '')
    primary_target_quantity = primary_target_info.get('quantity', 1)

    if primary_target_name in PRIMARY_TARGETS:
        primary_target_value = PRIMARY_TARGETS[primary_target_name]['hard' if is_hard_mode else 'normal']
    else:
        primary_target_value = 0

    result['Primary Target'] = {
        'name': primary_target_name,
        'value': primary_target_value * primary_target_quantity
    }

    return result


# # Example usage
# loot_info = {
#     'primary_target': {'name': 'Sinsimito Tequila'},
#     'gold': 2,
#     'cocaine': 2,
#     'weed': 2,
#     'painting': 1,
#     'cash': 6
# }

# players = 4

# is_hard_mode = True

# import json

# print(json.dumps(plan_loot_distribution(loot_info, players, is_hard_mode), indent=4))