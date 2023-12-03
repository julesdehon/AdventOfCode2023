_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
_ROOT_DIR="$(readlink -f "$_SCRIPT_DIR/../")"
source "$_ROOT_DIR/toolchain/colours.sh"

echo "Removing unused imports..."
autoflake --in-place --recursive --remove-all-unused-imports $_ROOT_DIR
echo "${GREEN}Removed unused imports${NO_COLOR}"

echo "Sorting imports..."
isort --atomic "$_ROOT_DIR"
echo "${GREEN}Sorted imports${NO_COLOR}"

echo "Formatting source code..."
black --preview "$_ROOT_DIR"
echo "${GREEN}Formatted source code${NO_COLOR}"