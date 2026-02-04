const form = document.getElementById("memberForm");
const table = document.getElementById("memberTable");
const count = document.getElementById("memberCount");

let members = [];

form.addEventListener("submit", function (e) {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const age = document.getElementById("age").value;
    const plan = document.getElementById("plan").value;

    members.push({ name, age, plan });

    updateTable();
    form.reset();
});

function updateTable() {
    table.innerHTML = "";
    members.forEach(member => {
        table.innerHTML += `
            <tr>
                <td>${member.name}</td>
                <td>${member.age}</td>
                <td>${member.plan}</td>
            </tr>
        `;
    });
    count.innerText = members.length;
}
