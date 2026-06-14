import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-pet-search',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './pet-search.component.html',
  styleUrls: ['./pet-search.component.css'],
})
export class PetSearchComponent {
  @Input() search = '';
  @Output() searchChange = new EventEmitter<string>();

  onInput(value: string): void {
    this.search = value;
    this.searchChange.emit(value);
  }

  clear(): void {
    this.search = '';
    this.searchChange.emit('');
  }
}
