{% macro ep_header(authors=['guiferviz'], status='', created='', version='') -%}
{{ exception("Unknown status") if status not in ["Planned", "Active", "Deprecated"] else "" }}
<style>
    #ep-table td img { 
      vertical-align: top;
      border-radius: 10px;
    }
</style>
<table id="ep-table">
    <tr>
        <td><strong>Authors:</strong></td>
        <td>
            {% for author in authors %}
                <a href="https://github.com/{{author}}">
                    <img src="https://github.com/{{author}}.png?size=20" alt="{{author}}'s profile picture">
                    {{author}}
                </a>
                {{ ", " if not loop.last else "" }}
            {% endfor %}
        </td>
    </tr>
    <tr>
        <td><strong>Status:</strong></td>
        <td>
        {% if status == "Planned" %}
            📅 Planned
        {% elif status == "Active" %}
            ✅ Active
        {% elif status == "Deprecated" %}
            📜 Deprecated
        {% endif %}
        </td>
    </tr>
    <tr>
        <td><strong>Created:</strong></td>
        <td>{{ created }}</td>
    </tr>
    <tr>
        <td><strong>Version:</strong></td>
        <td>{{ version }}</td>
    </tr>
</table>
{%- endmacro %}
