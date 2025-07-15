/* ==========================================================================
   File: upload.js
   Purpose: Handles drag-and-drop artwork uploads with progress feedback.
   ========================================================================== */

/**
 * Initialise upload handling once the DOM is ready.
 */
document.addEventListener('DOMContentLoaded', () => {
    const zone = document.getElementById('dropzone');
    const fileInput = document.getElementById('file-input');
    const list = document.getElementById('upload-list');
    const overlay = zone.querySelector('.spinner-overlay');

    /**
     * Create a list item with progress bar for a file.
     * @param {File} file
     * @returns {{file: File, li: HTMLElement, bar: HTMLElement, txt: HTMLElement}}
     */
    function createRow(file) {
        const li = document.createElement('li');
        li.textContent = file.name + ' ';
        const barWrap = document.createElement('div');
        barWrap.className = 'upload-progress';
        const bar = document.createElement('div');
        bar.className = 'upload-progress-bar';
        barWrap.appendChild(bar);
        const txt = document.createElement('span');
        txt.className = 'upload-percent';
        li.appendChild(barWrap);
        li.appendChild(txt);
        list.appendChild(li);
        return {file, li, bar, txt};
    }

    /**
     * Send a single file to the server.
     * @param {File} file
     * @param {Object} row Row elements returned from createRow
     * @returns {Promise<boolean>} success indicator
     */
    function uploadFile(file, row) {
        return new Promise(resolve => {
            const xhr = new XMLHttpRequest();
            const formData = new FormData();
            formData.append('images', file);
            xhr.open('POST', '/upload');
            xhr.setRequestHeader('Accept', 'application/json');
            xhr.upload.onprogress = e => {
                if (e.lengthComputable) {
                    const p = Math.round(e.loaded / e.total * 100);
                    row.bar.style.width = p + '%';
                    row.txt.textContent = p + '%';
                }
            };
            xhr.onload = () => {
                let ok = false;
                if (xhr.status === 200) {
                    try {
                        const res = JSON.parse(xhr.responseText)[0];
                        ok = !!res.success;
                        row.txt.textContent = ok ? 'Uploaded!' : (res.error || 'Failed');
                    } catch (err) {
                        row.txt.textContent = 'Error';
                    }
                } else {
                    row.txt.textContent = 'Error ' + xhr.status;
                }
                row.li.classList.add(ok ? 'success' : 'error');
                resolve(ok);
            };
            xhr.onerror = () => {
                row.li.classList.add('error');
                row.txt.textContent = 'Failed';
                resolve(false);
            };
            xhr.send(formData);
        });
    }

    /**
     * Preview and upload a set of files.
     * @param {FileList|File[]} files
     */
    async function handleFiles(files) {
        if (!files || !files.length) return;
        list.innerHTML = '';
        const rows = Array.from(files).map(createRow);
        overlay.classList.add('active');
        zone.classList.add('disabled');
        for (const row of rows) {
            await uploadFile(row.file, row);
        }
        overlay.classList.remove('active');
        zone.classList.remove('disabled');
        if (list.querySelector('li.success')) {
            const msg = document.createElement('li');
            msg.className = 'upload-success';
            msg.textContent = 'Success!';
            list.appendChild(msg);
            setTimeout(() => { window.location.href = '/artworks'; }, 800);
        }
    }

    if (!zone) return;

    ['dragenter','dragover'].forEach(evt => {
        zone.addEventListener(evt, e => {
            e.preventDefault();
            zone.classList.add('dragover');
        });
    });
    ['dragleave','drop'].forEach(evt => {
        zone.addEventListener(evt, () => zone.classList.remove('dragover'));
    });
    zone.addEventListener('drop', e => {
        e.preventDefault();
        handleFiles(e.dataTransfer.files);
    });
    zone.addEventListener('click', () => fileInput.click());
    zone.addEventListener('keypress', e => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            fileInput.click();
        }
    });
    fileInput.addEventListener('change', () => handleFiles(fileInput.files));
});
