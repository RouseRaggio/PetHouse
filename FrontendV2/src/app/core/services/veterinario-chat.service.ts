import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class VeterinarioChatService {

  private readonly apiUrl = 'http://localhost:8000/veterinario/chat';

  constructor(private readonly http: HttpClient) {}

  enviarMensaje(petId: number, mensaje: string) {
    return this.http.post(this.apiUrl, {
      pet_id: petId,
      mensaje: mensaje
    });
  }

}