export function formatAge(birthDateString) {
	if (!birthDateString) return 'Desconocida';
	
	const birthDate = new Date(birthDateString);
	if (isNaN(birthDate.getTime())) return 'Desconocida';
	
	const today = new Date();
	
	if (birthDate > today) return 'Fecha inválida';

	let years = today.getFullYear() - birthDate.getFullYear();
	let months = today.getMonth() - birthDate.getMonth();
	let days = today.getDate() - birthDate.getDate();

	if (days < 0) {
		months--;
		const prevMonth = new Date(today.getFullYear(), today.getMonth(), 0);
		days += prevMonth.getDate();
	}

	if (months < 0) {
		years--;
		months += 12;
	}

	if (years > 0) {
		if (months > 0) {
			return `${years} ${years === 1 ? 'año' : 'años'} y ${months} ${months === 1 ? 'mes' : 'meses'}`;
		}
		return `${years} ${years === 1 ? 'año' : 'años'}`;
	}

	if (months > 0) {
		if (days > 0) {
			return `${months} ${months === 1 ? 'mes' : 'meses'} y ${days} ${days === 1 ? 'día' : 'días'}`;
		}
		return `${months} ${months === 1 ? 'mes' : 'meses'}`;
	}

	if (days > 0) {
		return `${days} ${days === 1 ? 'día' : 'días'}`;
	}

	return 'Recién nacido';
}
