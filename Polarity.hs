module Polarity (polarity) where
type Assignment = [((Int, Int), Char)]

polarity :: [String] -> ([Int], [Int], [Int], [Int]) -> [String]
polarity board specs@(leftCons, rightCons, topCons, bottomCons) =
  let nrows    = length board
      ncols    = if nrows == 0 then 0 else length (head board)
      dominoes = buildDominoes board nrows ncols
      solution = solveDominoes dominoes [] nrows ncols specs
  in case solution of
       Just assign -> assignmentToStrings assign nrows ncols
       Nothing     -> error "No solution found"

buildDominoes :: [String] -> Int -> Int -> [((Int, Int), (Int, Int))]
buildDominoes board nrows ncols =
  [ ((r, c), partner) | 
  r <- [0 .. nrows - 1], 
  c <- [0 .. ncols - 1],
  let ch = (board !! r) !! c, 
  ch == 'L' || ch == 'T', 
  let partner = case ch of
                    'L' -> (r, c + 1)
                    'T' -> (r + 1, c)
                    _   -> error "Impossible" ]

solveDominoes :: [((Int, Int), (Int, Int))] -> Assignment -> Int -> Int -> ([Int],[Int],[Int],[Int]) -> Maybe Assignment
solveDominoes [] assign _ _ _ = Just assign
solveDominoes ((p1, p2):ds) assign nrows ncols specs =
  if memberA p1 assign || memberA p2 assign
    then solveDominoes ds assign nrows ncols specs
    else tryOptions options
  where
    options :: [(Char, Char)]
    options = [('X','X'), ('+','-'), ('-','+')]
    tryOptions [] = Nothing
    tryOptions ((v1,v2):opts) =
      let newAssign = insertA p1 v1 (insertA p2 v2 assign)
      in if checkPartial newAssign nrows ncols specs p1 &&
            checkPartial newAssign nrows ncols specs p2
         then case solveDominoes ds newAssign nrows ncols specs of
                Just sol -> Just sol
                Nothing  -> tryOptions opts
         else tryOptions opts

assignmentToStrings :: Assignment -> Int -> Int -> [String]
assignmentToStrings assign nrows ncols =
  [ [ fromMaybeA ' ' (lookupA (r, c) assign) | c <- [0 .. ncols - 1] ]
    | r <- [0 .. nrows - 1] ]

checkPartial :: Assignment -> Int -> Int -> ([Int],[Int],[Int],[Int]) -> (Int,Int) -> Bool
checkPartial assign nrows ncols specs (r, c) =
  checkAdjacencyCell assign (r, c) nrows ncols &&
  checkRowPartial assign ncols specs r &&
  checkColPartial assign nrows specs c

checkAdjacencyCell :: Assignment -> (Int,Int) -> Int -> Int -> Bool
checkAdjacencyCell assign (r,c) nrows ncols =
  let val = fromMaybeA ' ' (lookupA (r,c) assign)
      neighs = neighbors (r,c) nrows ncols
  in all (\p -> case lookupA p assign of
                  Just v  -> (val == 'X') || (v == 'X') || (val /= v)
                  Nothing -> True) neighs

neighbors :: (Int,Int) -> Int -> Int -> [(Int,Int)]
neighbors (r,c) nrows ncols =
  [ (x, y) | (x, y) <- [(r-1,c), (r+1,c), (r,c-1), (r,c+1)]
           , x >= 0, x < nrows, y >= 0, y < ncols ]

checkRowPartial :: Assignment -> Int -> ([Int],[Int],[Int],[Int]) -> Int -> Bool
checkRowPartial assign ncols (leftCons, rightCons, _, _) r =
  let rowVals = [ lookupA (r, c) assign | c <- [0..ncols-1] ]
      plusCount = length [ () | Just v <- rowVals, v == '+' ]
      minusCount = length [ () | Just v <- rowVals, v == '-' ]
      assignedCnt = length [ () | Just _ <- rowVals ]
      reqPlus  = leftCons !! r
      reqMinus = rightCons !! r
  in (reqPlus == -1 || plusCount <= reqPlus) &&
     (reqMinus == -1 || minusCount <= reqMinus) &&
     (assignedCnt < ncols ||
       ((reqPlus == -1 || plusCount == reqPlus) &&
        (reqMinus == -1 || minusCount == reqMinus)))

checkColPartial :: Assignment -> Int -> ([Int],[Int],[Int],[Int]) -> Int -> Bool
checkColPartial assign nrows (_,_,topCons,bottomCons) c =
  let colVals = [ lookupA (r, c) assign | r <- [0..nrows-1] ]
      plusCount = length [ () | Just v <- colVals, v == '+' ]
      minusCount = length [ () | Just v <- colVals, v == '-' ]
      assignedCnt = length [ () | Just _ <- colVals ]
      reqPlus  = topCons !! c
      reqMinus = bottomCons !! c
  in (reqPlus == -1 || plusCount <= reqPlus) &&
     (reqMinus == -1 || minusCount <= reqMinus) &&
     (assignedCnt < nrows ||
       ((reqPlus == -1 || plusCount == reqPlus) &&
        (reqMinus == -1 || minusCount == reqMinus)))

lookupA :: (Eq a) => a -> [(a, b)] -> Maybe b
lookupA _ [] = Nothing
lookupA key ((k,v):xs)
  | key == k  = Just v
  | otherwise = lookupA key xs

insertA :: (Eq a) => a -> b -> [(a, b)] -> [(a, b)]
insertA key value [] = [(key, value)]
insertA key value ((k,v):xs)
  | key == k  = (key, value) : xs
  | otherwise = (k,v) : insertA key value xs

memberA :: (Eq a) => a -> [(a,b)] -> Bool
memberA key [] = False
memberA key ((k,_):xs) = key == k || memberA key xs

fromMaybeA :: a -> Maybe a -> a
fromMaybeA def Nothing  = def
fromMaybeA _   (Just x) = x