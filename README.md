# Mathematical Algorithm for Optimal Loot Distribution in Cayo Perico Heist

## Overview

The optimal loot distribution problem in the GTA V Online Cayo Perico Heist can be modeled as a variation of the **Knapsack Problem**, which is a classic optimization problem in combinatorial optimization. The goal is to maximize the total value of loot collected by all players without exceeding the bag capacity constraints.

We employ a **greedy algorithm** approach to prioritize loot items based on their **value density** (value per unit of bag space). This method is practical and efficient for real-time decision-making within the game's context.

## Knapsack Problem Context

In the traditional Knapsack Problem:

- **Items**: Each item has a weight and a value.
- **Knapsack**: Has a maximum weight capacity.
- **Objective**: Maximize the total value of items in the knapsack without exceeding its capacity.

In our scenario:

- **Items**: Different types of loot (gold, cocaine, weed, painting, cash).
- **Weight**: Bag space occupied by the loot (percentage of the total capacity).
- **Value**: Monetary value of the loot.
- **Knapsacks**: The loot bags of each player, each with a capacity of 100%.

However, we have additional constraints:

- Loot must be collected in integer increments of clicks per stack.
- Each loot type has specific mechanics (e.g., paintings are collected in one action).

## Algorithm Steps

### 1. Define Loot Attributes

For each loot type $L$, define:

- $V_L$: Value per full stack.
- $B_L$: Bag space per full stack (as a percentage of total bag capacity).
- $C_L$: Number of clicks required to collect a full stack.

### 2. Calculate Value Density

Compute the **value density** $\rho_L$ for each loot type, which represents the value per 1% of bag space:

$$\rho_L = \frac{V_L}{B_L}$$

This metric helps prioritize loot types based on their efficiency in occupying bag space.

### 3. Prioritize Loot Types Using Greedy Approach

Sort the loot types in descending order of their value density $\rho_L$:

1. **Gold**
2. **Cocaine**
3. **Weed**
4. **Painting**
5. **Cash**

This greedy approach ensures that the highest value density loot is collected first.

### 4. Initialize Players and Loot Stacks

- **Players**: For each player $P_i$ , initialize their remaining bag capacity:

 $$R_i = 100\% $$

- **Loot Stacks**: For each available stack of loot type$L$:

  - $S_j$: The $j^\text{th}$ stack of loot type $L$.
  - Remaining clicks:  
$$r_{S_j} = C_L$$

### 5. Distribute Loot Among Players

For each loot type$L$in the priority list:

1. For each stack$S_j$of loot type$L$:

   a. While $r_{S_j} > 0$ :

      i. For each player $P_i$ with $R_i > 0$ :
         - **Bag Space per Click**:
          $$b_L = \frac{B_L}{C_L}$$
         - **Maximum Clicks Player Can Take**:
          $$k = \left\lfloor \frac{R_i}{b_L} \right\rfloor$$
         - **Clicks to Take**:
          $$c = \min(k, r_{S_j})$$
         - If $c \leq 0$ , skip to the next player.
         - **Update Player's Bag Capacity**:
          $$R_i = R_i - c \times b_L$$
         - **Record Loot Taken**:
           - Add$c$clicks from stack$S_j$to player$P_i$'s loot.
         - **Update Stack's Remaining Clicks**:
          $$r_{S_j} = r_{S_j} - c$$
         - Break if$R_i = 0$or$r_{S_j} = 0$.

      ii. If no player can take more from $S_j$ , move to the next stack.

### 6. Compile Results

For each player $P_i$:

- **Total Value Collected**:

 $$V_i = \sum_{L} \sum_{S_j} c_{i,L,S_j} \times v_L$$

  where $v_L = \frac{V_L}{C_L}$ is the value per click.

- **Total Bag Space Used**:
 $$B_i = 100\% - R_i$$

- **Loot Details**: Record the loot collected from each stack $S_j$ of each loot type $L$.

## Greedy Algorithm Justification

The greedy algorithm is suitable for this problem because:

- **Value Maximization**: Prioritizing loot based on value density aims to maximize the total value collected.
- **Simplicity and Efficiency**: The greedy approach is straightforward and computationally efficient, which is practical for real-time gameplay.
- **Integer Constraints**: Although the classic knapsack problem requires dynamic programming for optimal solutions, the greedy algorithm provides a near-optimal solution acceptable in the game's context.

## Example Calculation

### Loot Attributes

| Loot Type |$V_L$ (Value per Stack) |$B_L$ (Bag Space per Stack) |$C_L$ (Clicks per Stack) |
|-----------|-----------------------------|----------------------------------|------------------------------|
| Gold      |$330,000                    | 66.67%                           | 10                           |
| Cocaine   |$220,000                    | 50%                              | 10                           |
| Weed      |$145,000                    | 37.5%                            | 10                           |
| Painting  |$190,000                    | 50%                              | 1                            |
| Cash      |$90,000                     | 25%                              | 10                           |

### Calculating Value Density

- **Gold**:
 $$D_{\text{gold}} = \frac{330,000}{66.67} \approx 4,950 \text{ per 1% bag space}$$

- **Cocaine**:
 $$D_{\text{cocaine}} = \frac{220,000}{50} =  4,400 \text{ per 1% bag space}$$

- **Weed**:
 $$D_{\text{weed}} = \frac{145,000}{37.5} \approx 3,866.67 \text{ per 1% bag space}$$

- **Painting**:
 $$D_{\text{painting}} = \frac{190,000}{50} =  3,800 \text{ per 1% bag space}$$

- **Cash**:
 $$D_{\text{cash}} = \frac{90,000}{25} =  3,600 \text{ per 1% bag space}$$

### Distribute Loot Among Players

Assuming 4 players, we allocate loot starting from the highest priority:

#### Gold Allocation

- **Stacks**: $S_0$ and $S_1$, each with 10 clicks.
- **Bag Space per Click** for gold:

 $$b_{\text{gold}} = \frac{66.67\%}{10} = 6.667\%$$

- **Players**:

  - **Player 1**:
    - Can take $k = \left\lfloor \frac{100\%}{6.667\%} \right\rfloor = 15$ clicks.
    - Takes 10 clicks from $S_0$ (fully empties the stack).
    - Bag space used: $10 \times 6.667\% = 66.67\%$.
    - Remaining capacity: $R_1 = 33.33\%$.
  - **Player 2**:
    - Takes 10 clicks from $S_1$.
    - Remaining capacity: $R_2 = 33.33\%$.

#### Cocaine Allocation

- **Stacks**: $S_2$ and $S_3$ , each with 10 clicks.
- **Bag Space per Click** for cocaine:
 $$b_{\text{cocaine}} = \frac{50\%}{10} = 5\%$$

- **Player 1**:
  - Can take $k = \left\lfloor \frac{33.33\%}{5\%} \right\rfloor = 6$ clicks.
  - Takes 6 clicks from $S_2$.
  - Remaining capacity: $R_1 = 3.33\%$.
- **Player 2**:
  - Can take $k = 6$ clicks.
  - Takes remaining 4 clicks from $S_2$.
  - Remaining capacity: $R_2 = 13.33\%$.
- **Player 4**:
  - Takes 10 clicks from $S_3$.
  - Remaining capacity: $R_4 = 50\%$.

#### Continue Allocation with Weed, Painting, and Cash

- **Player 3**:
  - Collects the painting ($B_{\text{painting}} = 50\%$).
  - Remaining capacity: $R_3 = 50\%$.
- **Weed Allocation**:
  - **Bag Space per Click** for weed:

   $$b_{\text{weed}} = \frac{37.5\%}{10} = 3.75\%$$

  - **Player 3**:
    - Can take $k = \left\lfloor \frac{50\%}{3.75\%} \right\rfloor = 13$ clicks.
    - Takes 10 clicks from $S_4$ (fully empties the stack).
    - Remaining capacity: $R_3 = 12.5\%$.
  - **Player 4**:
    - Takes 10 clicks from $S_5$.
    - Remaining capacity: $R_4 = 12.5\%$.
- **Cash Allocation**:
  - **Bag Space per Click** for cash:

   $$b_{\text{cash}} = \frac{25\%}{10} = 2.5\% $$

  - **Player 2**:
    - Can take $k = \left\lfloor \frac{13.33\%}{2.5\%} \right\rfloor = 5$ clicks.
    - Takes 5 clicks from a cash stack.
    - Remaining capacity: $R_2 = 0.83\%$.
  - **Player 3**:
    - Takes 5 clicks from the same cash stack.
    - Remaining capacity: $R_3 = 0\%$.
  - **Player 4**:
    - Takes 5 clicks from another cash stack.
    - Remaining capacity: $R_4 = 0\%$.

### Compile Results

- **Player 1**:
  - Loot: Gold (10 clicks), Cocaine (6 clicks).
  - Total bag space used: $66.67\% + 30\% = 96.67\%$.
- **Player 2**:
  - Loot: Gold (10 clicks), Cocaine (4 clicks), Cash (5 clicks).
  - Total bag space used: $66.67\% + 20\% + 12.5\% = 99.17\%$.
- **Player 3**:
  - Loot: Painting (1 action), Weed (10 clicks), Cash (5 clicks).
  - Total bag space used: $50\% + 37.5\% + 12.5\% = 100\%$.
- **Player 4**:
  - Loot: Cocaine (10 clicks), Weed (10 clicks), Cash (5 clicks).
  - Total bag space used: $50\% + 37.5\% + 12.5\% = 100\%$.

## Limitations and Considerations

- **Integer Constraints**: The problem is an instance of the **0/1 Knapsack Problem** with additional integer constraints due to the clicks mechanism.
- **Greedy Algorithm Suboptimality**: While the greedy algorithm provides a practical solution, it may not always yield the absolute optimal result for the integer knapsack problem.
- **Game Mechanics**: The algorithm assumes that players can access all loot stacks, which may not always be feasible due to in-game restrictions.

## Conclusion

By combining the greedy algorithm with the knapsack problem framework, we achieve an effective method for optimizing loot distribution in the Cayo Perico Heist. This approach maximizes the total value collected by prioritizing loot types based on their value density and adhering to the game's mechanics of loot collection via clicks.
