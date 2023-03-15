/*
 *   This content is licensed according to the W3C Software License at
 *   https://www.w3.org/Consortium/Legal/2015/copyright-software-and-document
 * 
 *   https://www.w3.org/WAI/ARIA/apg/patterns/table/examples/sortable-table/
 *
 *   File:   sortable-table.js
 *
 *   Desc:   Adds sorting to a HTML data table that implements ARIA Authoring Practices
 */

// 'use strict';

// class SortableTable {
//   constructor(tableNode) {
//     this.tableNode = tableNode;

//     this.columnHeaders = tableNode.querySelectorAll('thead th');

//     this.sortColumns = [];

//     for (var i = 0; i < this.columnHeaders.length; i++) {
//       var ch = this.columnHeaders[i];
//       var buttonNode = ch.querySelector('button');
//       if (buttonNode) {
//         this.sortColumns.push(i);
//         buttonNode.setAttribute('data-column-index', i);
//         buttonNode.addEventListener('click', this.handleClick.bind(this));
//       }
//     }

//     this.optionCheckbox = document.querySelector(
//       'input[type="checkbox"][value="show-unsorted-icon"]'
//     );

//     if (this.optionCheckbox) {
//       this.optionCheckbox.addEventListener(
//         'change',
//         this.handleOptionChange.bind(this)
//       );
//       if (this.optionCheckbox.checked) {
//         this.tableNode.classList.add('show-unsorted-icon');
//       }
//     }
//   }

//   setColumnHeaderSort(columnIndex) {
//     if (typeof columnIndex === 'string') {
//       columnIndex = parseInt(columnIndex);
//     }

//     for (var i = 0; i < this.columnHeaders.length; i++) {
//       var ch = this.columnHeaders[i];
//       var buttonNode = ch.querySelector('button');
//       if (i === columnIndex) {
//         var value = ch.getAttribute('aria-sort');
//         if (value === 'descending') {
//           ch.setAttribute('aria-sort', 'ascending');
//           this.sortColumn(
//             columnIndex,
//             'ascending',
//             ch.classList.contains('num')
//           );
//         } else {
//           ch.setAttribute('aria-sort', 'descending');
//           this.sortColumn(
//             columnIndex,
//             'descending',
//             ch.classList.contains('num')
//           );
//         }
//       } else {
//         if (ch.hasAttribute('aria-sort') && buttonNode) {
//           ch.removeAttribute('aria-sort');
//         }
//       }
//     }
//   }

//   sortColumn(columnIndex, sortValue, isNumber) {
//     function compareValues(a, b) {
//       if (sortValue === 'ascending') {
//         if (a.value === b.value) {
//           return 0;
//         } else {
//           if (isNumber) {
//             return a.value - b.value;
//           } else {
//             return a.value < b.value ? -1 : 1;
//           }
//         }
//       } else {
//         if (a.value === b.value) {
//           return 0;
//         } else {
//           if (isNumber) {
//             return b.value - a.value;
//           } else {
//             return a.value > b.value ? -1 : 1;
//           }
//         }
//       }
//     }

//     if (typeof isNumber !== 'boolean') {
//       isNumber = false;
//     }

//     var tbodyNode = this.tableNode.querySelector('tbody');
//     var rowNodes = [];
//     var dataCells = [];

//     var rowNode = tbodyNode.firstElementChild;

//     var index = 0;
//     while (rowNode) {
//       rowNodes.push(rowNode);
//       var rowCells = rowNode.querySelectorAll('th, td');
//       var dataCell = rowCells[columnIndex];

//       var data = {};
//       data.index = index;
//       data.value = dataCell.textContent.toLowerCase().trim();
//       if (isNumber) {
//         data.value = parseFloat(data.value);
//       }
//       dataCells.push(data);
//       rowNode = rowNode.nextElementSibling;
//       index += 1;
//     }

//     dataCells.sort(compareValues);

//     // remove rows
//     while (tbodyNode.firstChild) {
//       tbodyNode.removeChild(tbodyNode.lastChild);
//     }

//     // add sorted rows
//     for (var i = 0; i < dataCells.length; i += 1) {
//       tbodyNode.appendChild(rowNodes[dataCells[i].index]);
//     }
//   }


    
//   /* EVENT HANDLERS */

//   handleClick(event) {
//     var tgt = event.currentTarget;
//     this.setColumnHeaderSort(tgt.getAttribute('data-column-index'));
//   }

//   handleOptionChange(event) {
//     var tgt = event.currentTarget;

//     if (tgt.checked) {
//       this.tableNode.classList.add('show-unsorted-icon');
//     } else {
//       this.tableNode.classList.remove('show-unsorted-icon');
//     }
//   }
// }

// // Initialize sortable table buttons
// window.addEventListener('load', function () {
//   var sortableTables = document.querySelectorAll('table.sortable');
//   for (var i = 0; i < sortableTables.length; i++) {
//     new SortableTable(sortableTables[i]);
//   }
// });



//Simple Sorting Method

//========== Date still needs to be sorted==========

const getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;

const comparer = (idx, asc) => (a, b) => ((v1, v2) => 
    v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2)
    )(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));

document.querySelectorAll('th').forEach(th => th.addEventListener('click', (() => {
  const table = th.closest('table');
  const tbody = table.querySelector('tbody');
  Array.from(tbody.querySelectorAll('tr'))
    .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
    .forEach(tr => tbody.appendChild(tr) );
})));


// Search function in players table

function searchFunction() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("searchInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("playerstable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

function searchFunctionClubs() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("searchInputClubs");
  filter = input.value.toUpperCase();
  table = document.getElementById("clubstable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}


