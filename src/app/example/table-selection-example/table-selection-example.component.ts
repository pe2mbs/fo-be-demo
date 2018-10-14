import { Component, OnInit, ViewChild } from '@angular/core';
import { SelectionModel, DataSource } from '@angular/cdk/collections';
import { MatTableDataSource, 
         MatPaginator, 
         MatSort, 
         MatTable} from '@angular/material';
import { Observable, merge, BehaviorSubject } from 'rxjs';
import { map } from 'rxjs/operators';

export interface PeriodicElement {
  name: string;
  position: number;
  weight: number;
  symbol: string;
}

const ELEMENT_DATA: PeriodicElement[] = [
  {position: 1, name: 'Hydrogen-bla', weight: 1.0079, symbol: 'H'},
  {position: 2, name: 'Helium', weight: 4.0026, symbol: 'He'},
  {position: 3, name: 'Lithium', weight: 6.941, symbol: 'Li'},
  {position: 4, name: 'Beryllium', weight: 9.0122, symbol: 'Be'},
  {position: 5, name: 'Boron', weight: 10.811, symbol: 'B'},
  {position: 6, name: 'Carbon', weight: 12.0107, symbol: 'C'},
  {position: 7, name: 'Nitrogen', weight: 14.0067, symbol: 'N'},
  {position: 8, name: 'Oxygen', weight: 15.9994, symbol: 'O'},
  {position: 9, name: 'Fluorine', weight: 18.9984, symbol: 'F'},
  {position: 10, name: 'Neon', weight: 20.1797, symbol: 'Ne'},
  {position: 11, name: 'Hydrogen-bla', weight: 1.0079, symbol: 'H'},
  {position: 12, name: 'Helium', weight: 4.0026, symbol: 'He'},
  {position: 13, name: 'Lithium', weight: 6.941, symbol: 'Li'},
  {position: 14, name: 'Beryllium', weight: 9.0122, symbol: 'Be'},
  {position: 15, name: 'Boron', weight: 10.811, symbol: 'B'},
  {position: 16, name: 'Carbon', weight: 12.0107, symbol: 'C'},
  {position: 17, name: 'Nitrogen', weight: 14.0067, symbol: 'N'},
  {position: 18, name: 'Oxygen', weight: 15.9994, symbol: 'O'},
  {position: 19, name: 'Fluorine', weight: 18.9984, symbol: 'F'},
  {position: 20, name: 'Neon', weight: 20.1797, symbol: 'Ne'},
];

/**
 * Data source for the DataTable view. This class should
 * encapsulate all logic for fetching and manipulating the displayed data
 * (including sorting, pagination, and filtering).
 */
export class PeriodicTableDataSource extends DataSource<PeriodicElement> {
  dataStream = new BehaviorSubject<PeriodicElement[]>( ELEMENT_DATA );

  set data(v: PeriodicElement[]) { this.dataStream.next(v); }
  get data(): PeriodicElement[] { return this.dataStream.value; }

  constructor(private paginator: MatPaginator, private sort: MatSort) {
    super();
  }

  addData() {
    const copiedData = this.data.slice();    
    copiedData.push( {  position: 21,
                        name: 'Uranium',
                        weight: 21.1797, 
                        symbol: 'U' } );
    this.data = copiedData;
    console.log(this.data);
  }

  /**
   * Connect this data source to the table. The table will only update when
   * the returned stream emits new items.
   * @returns A stream of the items to be rendered.
   */
  connect(): Observable<PeriodicElement[]> {
    // Combine everything that affects the rendered data into one update
    // stream for the data-table to consume.
    const dataMutations = [
      this.dataStream,
      this.paginator.page,
      this.sort.sortChange
    ];

    // Set the paginators length
    this.paginator.length = this.data.length;

    return merge(...dataMutations).pipe(map(() => {
      return this.getPagedData(this.getSortedData([...this.data]));
    }));
  }

  /**
   *  Called when the table is being destroyed. Use this function, to clean up
   * any open connections or free any held resources that were set up during connect.
   */
  disconnect() {}

  /**
   * Paginate the data (client-side). If you're using server-side pagination,
   * this would be replaced by requesting the appropriate data from the server.
   */
  private getPagedData(data: PeriodicElement[]) {
    const startIndex = this.paginator.pageIndex * this.paginator.pageSize;
    return data.splice(startIndex, this.paginator.pageSize);
  }

  /**
   * Sort the data (client-side). If you're using server-side sorting,
   * this would be replaced by requesting the appropriate data from the server.
   */
  private getSortedData(data: PeriodicElement[]) {
    if (!this.sort.active || this.sort.direction === '') {
      return data;
    }

    return data.sort((a, b) => {
      const isAsc = this.sort.direction === 'asc';
      switch (this.sort.active) {
        case 'name': return compare(a.name, b.name, isAsc);
        case 'id': return compare(+a.position, +b.position, isAsc);
        default: return 0;
      }
    });
  }
}

/** Simple sort comparator for example ID/Name columns (for client-side sorting). */
function compare(a, b, isAsc) {
  return (a < b ? -1 : 1) * (isAsc ? 1 : -1);
}

@Component({
  selector: 'app-table-selection-example',
  templateUrl: './table-selection-example.component.html',
  styleUrls: ['./table-selection-example.component.css']
})
export class TableSelectionExampleComponent implements OnInit {

  displayedColumns: string[] = ['select', 'position', 'name', 'weight', 'symbol'];
  dataSource: PeriodicTableDataSource;
  selection = new SelectionModel<PeriodicElement>(true, []);
  @ViewChild( MatPaginator )  paginator:  MatPaginator;
  @ViewChild( MatSort )       sort:       MatSort;
  @ViewChild( MatTable )      matTable: MatTable<PeriodicElement>;
  constructor()
  {
  
  } 

  ngOnInit(): void
  {
    this.dataSource = new PeriodicTableDataSource( this.paginator, this.sort );
    return;
  }
  
  applyFilter(filterValue: string): void
  {
    /*
    this.dataSource.filter = filterValue.trim().toLowerCase();
    if (this.dataSource.paginator) 
    {
      this.dataSource.paginator.firstPage();
    }
    */
    return;
  }

  get editDisabled(): boolean
  {
    return this.selection.selected.length !== 1;
  }

  get addDisabled(): boolean
  {
    return this.selection.selected.length !== 0;
  }

  get deleteDisabled(): boolean
  {
    return this.selection.selected.length === 0;
  }

  /** Whether the number of selected elements matches the total number of rows. */
  isAllSelected(): boolean 
  {
    const numSelected = this.selection.selected.length;
    const numRows = this.dataSource.data.length;
    return numSelected === numRows;
  }

  /** Selects all rows if they are not all selected; otherwise clear selection. */
  masterToggle(): void 
  {
    this.isAllSelected() ? this.selection.clear() :
        this.dataSource.data.forEach( row => this.selection.select( row ) );
    return;
  }

  public addRecord(): void
  {
    this.dataSource.addData();
    this.matTable.renderRows();
    return;
  }

  public editRecord(): void
  {
    
    return;
  }

  public deleteRecord(): void
  {
    this.dataSource.data.pop();
    this.matTable.renderRows();
    return;
  }  
}
