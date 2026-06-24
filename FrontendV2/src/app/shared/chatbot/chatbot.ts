import { Component, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { ChatService } from '../../core/services/chat';

@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chatbot.html',
  styleUrls: ['./chatbot.css'],
})
export class ChatbotComponent {
  abierto = false;

  mensaje = '';

  mensajes: any[] = [];

  constructor(
    private chatService: ChatService,
    private cdr: ChangeDetectorRef,
  ) {}

  toggleChat() {
    this.abierto = !this.abierto;
  }

  enviar() {
    if (!this.mensaje.trim()) {
      return;
    }

    const texto = this.mensaje;

    // Mensaje usuario
    this.mensajes.push({
      tipo: 'usuario',
      texto,
    });

    this.mensaje = '';

    // Mensaje temporal
    const mensajeTemporal = {
      tipo: 'bot',
      texto: '🐾 PetHouse IA está escribiendo...',
    };

    this.mensajes.push(mensajeTemporal);

    this.cdr.detectChanges();

    this.chatService.enviarMensaje(texto).subscribe({
      next: (resp: any) => {
        console.log('RESPUESTA IA:', resp);

        // Reemplazar mensaje temporal
        mensajeTemporal.texto = resp.respuesta;

        this.cdr.detectChanges();

        setTimeout(() => {
          const contenedor = document.querySelector('.messages');

          if (contenedor) {
            contenedor.scrollTop = contenedor.scrollHeight;
          }
        }, 50);
      },

      error: (error) => {
        console.error('Error IA:', error);

        mensajeTemporal.texto = '❌ Lo siento, ocurrió un error al procesar tu solicitud.';

        this.cdr.detectChanges();
      },
    });
  }
}
