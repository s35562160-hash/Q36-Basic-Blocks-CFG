
import re

# Read Three Address Code instructions
def read_tac():
    print("Enter Three Address Code (type END to finish):")
    lines = []

    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        if line.strip():
            lines.append(line.strip())

    return lines


# Separate labels and instructions
def parse_tac(lines):
    instructions = []
    labels = {}

    for line in lines:
        text = line.strip()

        match = re.match(r'^([A-Za-z_]\w*)\s*:\s*(.*)$', text)

        if match:
            label = match.group(1)
            text = match.group(2).strip()
            labels[label] = len(instructions)

        if text:
            instructions.append(text)

    return instructions, labels


# Identify jump instructions
def get_jump(inst):
    match = re.match(
        r'^if\b.*?\bgoto\s+([A-Za-z_]\w*)\s*$',
        inst, re.IGNORECASE
    )

    if match:
        return "conditional", match.group(1)

    match = re.match(
        r'^goto\s+([A-Za-z_]\w*)\s*$',
        inst, re.IGNORECASE
    )

    if match:
        return "unconditional", match.group(1)

    return None, None


# Check return or stop instructions
def is_exit(inst):
    return bool(re.match(r'^(return|stop|halt)\b', inst, re.IGNORECASE))


# Find leaders of basic blocks
def find_leaders(instructions, labels):
    leaders = {0}
    n = len(instructions)

    for i, inst in enumerate(instructions):
        kind, target = get_jump(inst)

        if target:
            if target not in labels:
                raise ValueError("Undefined label: " + target)

            target_index = labels[target]

            if target_index >= n:
                raise ValueError("Label has no instruction: " + target)

            leaders.add(target_index)

            if i + 1 < n:
                leaders.add(i + 1)

        elif is_exit(inst):
            if i + 1 < n:
                leaders.add(i + 1)

    return sorted(leaders)


# Divide instructions into basic blocks
def create_blocks(instructions, leaders):
    blocks = []
    index_to_block = {}

    for i, start in enumerate(leaders):
        end = leaders[i + 1] if i + 1 < len(leaders) else len(instructions)

        block_number = i + 1
        block = instructions[start:end]

        blocks.append(block)

        for j in range(start, end):
            index_to_block[j] = block_number

    return blocks, index_to_block


# Generate Control Flow Graph edges
def generate_cfg(instructions, labels, blocks, leaders, index_to_block):
    edges = set()

    for i, block in enumerate(blocks):
        block_number = i + 1
        last_inst = block[-1]

        kind, target = get_jump(last_inst)

        if kind == "conditional":
            target_block = index_to_block[labels[target]]
            edges.add((block_number, target_block))

            if block_number < len(blocks):
                edges.add((block_number, block_number + 1))

        elif kind == "unconditional":
            target_block = index_to_block[labels[target]]
            edges.add((block_number, target_block))

        elif is_exit(last_inst):
            pass

        elif block_number < len(blocks):
            edges.add((block_number, block_number + 1))

    return sorted(edges)


# Main program
def main():
    lines = read_tac()

    if not lines:
        print("No instructions entered.")
        return

    try:
        instructions, labels = parse_tac(lines)

        leaders = find_leaders(instructions, labels)

        blocks, index_to_block = create_blocks(
            instructions, leaders
        )

        edges = generate_cfg(
            instructions, labels, blocks,
            leaders, index_to_block
        )

        print("\nLEADERS:")
        for leader in leaders:
            print("Instruction", leader + 1)

        print("\nBASIC BLOCKS:")
        for i, block in enumerate(blocks):
            print("\nB", i + 1, ":", sep="")
            for inst in block:
                print("  ", inst)

        print("\nCONTROL FLOW GRAPH EDGES:")
        for source, destination in edges:
            print("B" + str(source) + " -> B" + str(destination))

        if not edges:
            print("No CFG edges.")

    except ValueError as error:
        print("Error:", error)


if __name__ == "__main__":
    main()    
