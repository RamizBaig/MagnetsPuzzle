#![allow(non_snake_case, non_camel_case_types, dead_code)]

#[derive(Clone, Copy, PartialEq)]#[repr(u8)]
enum Orientation {Top,Bottom,Left,Right}
#[derive(Clone, Copy, PartialEq)]#[repr(u8)]
enum CellState {Positive,Negative,Empty,NoDominoe}

fn polarity(board: &[&str], specs: &(Vec<i32>, Vec<i32>, Vec<i32>, Vec<i32>)) -> Vec<String> {
    let mut puzzleStruct = buildPuzzle(board, specs);
    solveRecursively(&mut puzzleStruct);
    outputSolution(&puzzleStruct)
}

fn solveRecursively(puzzle: &mut Puzzle) -> bool {
    if puzzle.moves.is_empty() {return true}
    let index = puzzle.moves.pop().unwrap();
    let states = &[CellState::Empty, CellState::Positive, CellState::Negative];
    for &state in states {
        if isValidPlacement(puzzle, index, state) {
            updateConstraints(puzzle, index, state);
            if solveRecursively(puzzle) {return true}
            undoConstraints(puzzle, index, state);
        }   
    }
    puzzle.moves.push(index);
    false
}

fn isValidPlacement(puzzle: &Puzzle, index: usize, cellState: CellState) -> bool {
    let isValid = 
    match puzzle.board[index] {
        Orientation::Left => validHorizontalDominoe(puzzle, index, cellState),
        Orientation::Top => validVerticalDominoe(puzzle, index, cellState),
        _ => false};
    isValid
}

fn validHorizontalDominoe(puzzle: &Puzzle, index: usize, cellState: CellState) -> bool {
    let oppCellState = oppositeCellState(cellState);
    let oppIndex = getOppIndex(puzzle, index);
    let row = index / puzzle.width;
    let col = index % puzzle.width;
    let oppRow = oppIndex / puzzle.width;
    let oppCol = oppIndex % puzzle.width;

    if !checkNeighbors(puzzle, row, col, cellState){return false}
    if !checkNeighbors(puzzle, oppRow, oppCol, oppCellState){return false}

    if cellState == CellState::Empty {
        if puzzle.horizontalRemaining[row] - 2 < puzzle.leftConstraints[row].max(0)+puzzle.rightConstraints[row].max(0) {return false}
        if puzzle.verticalRemaining[col] - 1 < puzzle.topConstraints[col] {return false}
        if puzzle.verticalRemaining[col] - 1 < puzzle.bottomConstraints[col] {return false} // was this not work properly?
        if puzzle.verticalRemaining[oppCol] - 1 < puzzle.topConstraints[oppCol] {return false}
        if puzzle.verticalRemaining[oppCol] - 1 < puzzle.bottomConstraints[oppCol] {return false}
        return true
    }
    
    if puzzle.leftConstraints[row] == 0 {return false}
    if puzzle.rightConstraints[row] == 0 {return false}
    if puzzle.horizontalRemaining[row] - 2 < (puzzle.leftConstraints[row]-1).max(0)+(puzzle.rightConstraints[row]-1).max(0) {return false}

    if cellState == CellState::Positive {
        if puzzle.topConstraints[col] == 0 {return false}
        if puzzle.bottomConstraints[oppCol] == 0 {return false}
        if puzzle.verticalRemaining[col]-1 < puzzle.bottomConstraints[col] {return false}
        if puzzle.verticalRemaining[col] < puzzle.topConstraints[col] {return false}
        if puzzle.verticalRemaining[oppCol] < puzzle.bottomConstraints[oppCol] {return false}
        if puzzle.verticalRemaining[oppCol]-1 < puzzle.topConstraints[oppCol] {return false}
    }
    if cellState == CellState::Negative {
        if puzzle.topConstraints[oppCol] == 0 {return false}
        if puzzle.bottomConstraints[col] == 0 {return false}
        if puzzle.verticalRemaining[col]-1 < puzzle.topConstraints[col] {return false}
        if puzzle.verticalRemaining[col] < puzzle.bottomConstraints[col] {return false}
        if puzzle.verticalRemaining[oppCol] < puzzle.topConstraints[oppCol] {return false}
        if puzzle.verticalRemaining[oppCol]-1 < puzzle.bottomConstraints[oppCol] {return false}
    }

    true
}

fn validVerticalDominoe(puzzle: &Puzzle, index: usize, cellState: CellState) -> bool {
    let oppCellState = oppositeCellState(cellState);
    let oppIndex = getOppIndex(puzzle, index);
    let row = index / puzzle.width;
    let col = index % puzzle.width;
    let oppRow = oppIndex / puzzle.width;
    let oppCol = oppIndex % puzzle.width;
    if !checkNeighbors(puzzle, row, col, cellState){return false}
    if !checkNeighbors(puzzle, oppRow, oppCol, oppCellState){return false}
    if cellState == CellState::Empty {
        if puzzle.verticalRemaining[col] - 2 < puzzle.topConstraints[col].max(0)+puzzle.bottomConstraints[col].max(0) {return false}
        if puzzle.horizontalRemaining[row] - 1 < puzzle.leftConstraints[row] {return false}
        if puzzle.horizontalRemaining[row] - 1 < puzzle.rightConstraints[row] {return false}
        if puzzle.horizontalRemaining[oppRow] - 1 < puzzle.leftConstraints[oppRow] {return false}
        if puzzle.horizontalRemaining[oppRow] - 1 < puzzle.rightConstraints[oppRow] {return false}
        return true
    }

    if puzzle.topConstraints[col] == 0 {return false}
    if puzzle.bottomConstraints[col] == 0 {return false}
    if puzzle.verticalRemaining[col] - 2 < (puzzle.topConstraints[col]-1).max(0)+(puzzle.bottomConstraints[col]-1).max(0) {return false}

    if cellState == CellState::Positive {
        if puzzle.leftConstraints[row] == 0 {return false}
        if puzzle.rightConstraints[oppRow] == 0 {return false}
        if puzzle.horizontalRemaining[row]-1 < puzzle.rightConstraints[row] {return false}
        if puzzle.horizontalRemaining[row] < puzzle.leftConstraints[row] {return false}
        if puzzle.horizontalRemaining[oppRow] < puzzle.rightConstraints[oppRow] {return false}
        if puzzle.horizontalRemaining[oppRow]-1 < puzzle.leftConstraints[oppRow] {return false}
    }
    if cellState == CellState::Negative {
        if puzzle.leftConstraints[oppRow] == 0 {return false}
        if puzzle.rightConstraints[row] == 0 {return false}
        if puzzle.horizontalRemaining[row]-1 < puzzle.leftConstraints[row] {return false}
        if puzzle.horizontalRemaining[row] < puzzle.rightConstraints[row] {return false}
        if puzzle.horizontalRemaining[oppRow] < puzzle.leftConstraints[oppRow] {return false}
        if puzzle.horizontalRemaining[oppRow]-1 < puzzle.rightConstraints[oppRow] {return false}
    }
    
    true
}
#[inline]
fn checkNeighbors(puzzle: &Puzzle, row: usize, col: usize, cellState: CellState) -> bool {
    if cellState == CellState::Empty{return true}
    if row > 0 {
        let up = (row - 1) * puzzle.width + col;
        if puzzle.solution[up] == cellState {return false}
    }
    if row < puzzle.height - 1 {
        let down = (row + 1) * puzzle.width + col;
        if puzzle.solution[down] == cellState {return false}
    }
    if col > 0 {
        let left = row * puzzle.width + (col - 1);
        if puzzle.solution[left] == cellState {return false}
    }
    if col < puzzle.width - 1 {
        let right = row * puzzle.width + (col + 1);
        if puzzle.solution[right] == cellState {return false}
    }
    true
}

fn updateConstraints(puzzle: &mut Puzzle, index: usize, cellState: CellState) {
    let partnerIndex = getOppIndex(puzzle, index);
    let oppState = oppositeCellState(cellState);    
    let row = index / puzzle.width;
    let col = index % puzzle.width;
    let oppRow = partnerIndex / puzzle.width;
    let oppCol = partnerIndex % puzzle.width;
    
    puzzle.solution[index] = cellState;
    puzzle.solution[partnerIndex] = oppState;

    puzzle.verticalRemaining[col]-=1;
    puzzle.horizontalRemaining[row]-=1;
    puzzle.verticalRemaining[oppCol]-=1;
    puzzle.horizontalRemaining[oppRow]-=1;

    match cellState {
        CellState::Positive => {
            puzzle.topConstraints[col]-=1;
            puzzle.leftConstraints[row]-=1;
            puzzle.bottomConstraints[oppCol]-=1;
            puzzle.rightConstraints[oppRow]-=1;},
        CellState::Negative => {
            puzzle.topConstraints[oppCol]-=1;
            puzzle.leftConstraints[oppRow]-=1;
            puzzle.bottomConstraints[col]-=1;
            puzzle.rightConstraints[row]-=1;},
        _ => {}
    };
}

fn undoConstraints(puzzle: &mut Puzzle, index: usize, cellState: CellState) {
    let partnerIndex = getOppIndex(puzzle, index);
    let row = index / puzzle.width;
    let col = index % puzzle.width;
    let oppRow = partnerIndex / puzzle.width;
    let oppCol = partnerIndex % puzzle.width;

    puzzle.solution[index] = CellState::NoDominoe;
    puzzle.solution[partnerIndex] = CellState::NoDominoe;

    puzzle.verticalRemaining[col] += 1;
    puzzle.horizontalRemaining[row] += 1;
    puzzle.verticalRemaining[oppCol] += 1;
    puzzle.horizontalRemaining[oppRow] += 1;

    match cellState {
        CellState::Positive => {
            puzzle.topConstraints[col] += 1;
            puzzle.leftConstraints[row] += 1;
            puzzle.bottomConstraints[oppCol] += 1;
            puzzle.rightConstraints[oppRow] += 1;},
        CellState::Negative => {
            puzzle.topConstraints[oppCol] += 1;
            puzzle.leftConstraints[oppRow] += 1;
            puzzle.bottomConstraints[col] += 1;
            puzzle.rightConstraints[row] += 1;},
        _ => {}
    }
}

fn outputSolution(puzzle: &Puzzle) -> Vec<String> {
    let mut rows = Vec::with_capacity(puzzle.height);
    for r in 0..puzzle.height {
        let mut rowStr = String::with_capacity(puzzle.width);
        for c in 0..puzzle.width {
            let index = r * puzzle.width + c;
            let ch = match puzzle.solution[index] {
                CellState::Positive => '+',
                CellState::Negative => '-',
                _                   => 'X',
            };
            rowStr.push(ch);
        }
        rows.push(rowStr);
    }
    rows
}
#[inline]
fn oppositeCellState(state: CellState) -> CellState {
    match state {
        CellState::Positive => CellState::Negative,
        CellState::Negative => CellState::Positive,
        _ => CellState::Empty,
    }
}
#[inline]
fn getOppIndex(puzzle: &Puzzle, index: usize) -> usize {
    return match puzzle.board[index] {
        Orientation::Left => {index + 1}
        Orientation::Top => {index + puzzle.width}
        Orientation::Right => {index - 1}
        Orientation::Bottom => {index - puzzle.width}
    };
}

fn buildPuzzle(board: &[&str],specs: &(Vec<i32>, Vec<i32>, Vec<i32>, Vec<i32>)) -> Puzzle {
    let height = board.len();
    let width = board[0].len();
    let mut boardVec = Vec::with_capacity(width * height);
    for row in board {
        for ch in row.chars() {
            let orient = match ch {
                'T' => Orientation::Top,
                'B' => Orientation::Bottom,
                'L' => Orientation::Left,
                'R' => Orientation::Right,
                _ => unreachable!("impossible character"),
            };
            boardVec.push(orient);
        }
    }
    let solution = vec![CellState::NoDominoe; width * height];
    
    let (leftConstraints_i32, rightConstraints_i32, topConstraints_i32, bottomConstraints_i32) = &*specs;

    let leftConstraints: Vec<i8> = leftConstraints_i32.iter().map(|&x| x as i8).collect();
    let rightConstraints: Vec<i8> = rightConstraints_i32.iter().map(|&x| x as i8).collect();
    let topConstraints: Vec<i8> = topConstraints_i32.iter().map(|&x| x as i8).collect();
    let bottomConstraints: Vec<i8> = bottomConstraints_i32.iter().map(|&x| x as i8).collect();
    

    let verticalRemaining: Vec<i8> = vec![height as i8; width];
    let horizontalRemaining: Vec<i8> = vec![width as i8; height];

    let mut puzzle = Puzzle {
        width, height, board: boardVec, solution, moves: Vec::new(), leftConstraints, rightConstraints, 
        topConstraints, bottomConstraints, verticalRemaining, horizontalRemaining};
    puzzle.moves = computeMoveOrder(&puzzle);
    puzzle
}

fn computeMoveOrder(puzzle: &Puzzle) -> Vec<usize> {
    let width = puzzle.width;
    let height = puzzle.height;
    let totalCells = width * height;

    let mut moves = Vec::new();
    let mut added = vec![false; totalCells];
    for row in 0..height {
        let rowWeight = if puzzle.leftConstraints[row] == -1 && puzzle.rightConstraints[row] == -1 {
            (width / 2) as i8
        } else {
            let leftVal = if puzzle.leftConstraints[row] == -1 { 0 } else { puzzle.leftConstraints[row] };
            let rightVal = if puzzle.rightConstraints[row] == -1 { 0 } else { puzzle.rightConstraints[row] };
            leftVal + rightVal
        };
        if rowWeight == 0 as i8 {
            for col in 0..width {
                let index = row * width + col;
                let candidate = match puzzle.board[index] {
                    Orientation::Left | Orientation::Top => index,
                    _ => getOppIndex(puzzle, index)};
                if !added[candidate] {
                    moves.push(candidate);
                    added[candidate] = true
                }
            }
        }
    }
    for col in 0..width {
        let colWeight = if puzzle.topConstraints[col] == -1 && puzzle.bottomConstraints[col] == -1 {
            (width / 2) as i8
        } else {
            let topVal = if puzzle.topConstraints[col] == -1 { 0 } else { puzzle.topConstraints[col] };
            let bottomVal = if puzzle.bottomConstraints[col] == -1 { 0 } else { puzzle.bottomConstraints[col] };
            topVal + bottomVal
        };
        if colWeight == 0 as i8 {
            for row in 0..height {
                let index = row * width + col;
                let candidate = match puzzle.board[index] {
                    Orientation::Left | Orientation::Top => index,
                    _ => getOppIndex(puzzle, index),
                };
                if !added[candidate] {
                    moves.push(candidate);
                    added[candidate] = true;
                }
            }
        }
    }

    for i in 0..(width * height) {
        match puzzle.board[i] {
            Orientation::Top | Orientation::Left => {},
            _ => continue,
        }
        if !added[i] {
            moves.push(i);
            added[i] = true;
        }
    }
    moves.reverse();
    moves
}

struct Puzzle {
    width: usize,
    height: usize,
    board: Vec<Orientation>,   
    solution: Vec<CellState>,  
    moves: Vec<usize>,         

    leftConstraints: Vec<i8>,   
    rightConstraints: Vec<i8>,  
    topConstraints: Vec<i8>,    
    bottomConstraints: Vec<i8>, 

    verticalRemaining: Vec<i8>,    
    horizontalRemaining: Vec<i8>,   
}

#[cfg(test)]
#[path = "tests.rs"]
mod tests;