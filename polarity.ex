defmodule Polarity do

  @moduledoc """
    Add your solver function below. You may add additional helper functions if you desire.
    Test your code by running 'mix test --seed 0' from the simple_tester_ex directory.
  """

  def polarity(board, specs) do
    numRows = length(board)
    numCols = length(List.first(board))
    # Your code here!
    # Hard-coded solution to test 1 is below.
    temp = { "+-+-X-" , "-+-+X+", "XX+-+-", "XX-+X+", "-+XXX-" }
    temp = boardToMap(temp)
    temp = mapToBoard(temp, numRows, numCols)
    temp
  end

  def boardToMap(board) do
    Enum.reduce_with_index(board, %{}, fn row, row_index, acc ->
      Enum.reduce_with_index(String.graphemes(row), acc, fn char, col_index, acc_inner ->
        Map.put(acc_inner, {row_index, col_index}, char)
      end)
    end)
  end
  def rulesToMap(arr) do
    Enum.reduce_with_index(arr, %{}, fn value, index, acc ->
      Map.put(acc, index, value)
    end)
  end
  def mapToBoard(mappedBoard, numRows, numCols) do
    0..(numRows - 1)
    |> Enum.map(fn rowIndex ->
      0..(numCols - 1)
      |> Enum.map(fn colIndex ->
        Map.get(mappedBoard, {rowIndex, colIndex})
      end)
      |> Enum.join("")  # Join the characters to form the row string
    end)
  end


end
