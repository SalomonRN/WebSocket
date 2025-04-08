export const arrayBufferToFile = (buffer: ArrayBuffer, type: string) => {
    const blob = new Blob([buffer], { type: type });
    return URL.createObjectURL(blob);
};

export const arrayBufferToVideo = (buffer: ArrayBuffer) => {
    const blob = new Blob([buffer], { type: "video/mp4" });
    return URL.createObjectURL(blob);
};

export const arrayBufferToPDF = (buffer: ArrayBuffer) => {
    const blob = new Blob([buffer], { type: "application/pdf" });
    return URL.createObjectURL(blob);
};

export const arrayBufferToText = (buffer: ArrayBuffer) => {
    return new TextDecoder().decode(new Uint8Array(buffer));
};

export const downloadFile = (buffer: ArrayBuffer, filename: string, mimeType: string) => {
    const blob = new Blob([buffer], { type: mimeType });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
};

export const handleUpload = (file: File | null | undefined): Promise<Uint8Array | null> => {
    return new Promise((resolve) => {
        if (!file) {
            resolve(null); // No file selected
            return;
        }

        const reader = new FileReader();
        reader.readAsArrayBuffer(file);
        reader.onload = () => {
            if (reader.result) {
                const buffer = new Uint8Array(reader.result as ArrayBuffer);
                resolve(buffer); // Return the buffer
            } else {
                alert("???")
                resolve(null);
            }
        };
        reader.onerror = () => {
            console.error("Error reading file");
            resolve(null);
        };
    });
};
