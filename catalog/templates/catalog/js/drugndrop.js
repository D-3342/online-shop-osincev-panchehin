const list = document.getElementById('sortable-list');
let draggedItem = null;

list.addEventListener('dragstart', (e) => {
  draggedItem = e.target;
  e.dataTransfer.effectAllowed = 'move';
});

list.addEventListener('dragover', (e) => {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
});

list.addEventListener('drop', (e) => {
  e.preventDefault();

  const targetItem = e.target.closest('li');

  // Если тащили тот же элемент или сброс вне списка — ничего не делаем
  if (!draggedItem || !targetItem || draggedItem === targetItem) return;

  // Меняем элементы местами в DOM
  const parent = draggedItem.parentNode;
  const children = Array.from(parent.children);
  const draggedIndex = children.indexOf(draggedItem);
  const targetIndex = children.indexOf(targetItem);

  if (draggedIndex < targetIndex) {
    // Перемещаем после целевого
    targetItem.after(draggedItem);
  } else {
    // Перемещаем перед целевым
    targetItem.before(draggedItem);
  }

  // После перестановки — сохраняем новый порядок
  saveOrder();
});

// Очищаем переменную после окончания перетаскивания
list.addEventListener('dragend', () => {
  draggedItem = null;
});