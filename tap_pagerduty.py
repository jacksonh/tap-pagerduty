
import pypd
import singer
from singer import utils

REQUIRED_CONFIG_KEYS = ["start_date", "api_key"]

def get_pagerduty_incidents(config):
    res = []
    pypd.api_key = config.get('api_key')
    incidents = pypd.Incident.find(since=config.get('start_date'))
    for incident in incidents:
        res.append({
            'id': str(incident.json['id']),
            'status': str(incident.json['status']),
            'summary': str(incident.json['summary']),
            'url': str(incident.json['html_url']),
            'last_status_change_by': str(incident.json['last_status_change_by']['summary']),
            'created_at': str(incident.json['created_at']),
            'last_updated_at': str(incident.json['last_status_change_at'])
        })
    return res

def schema():
    return {
        'properties':   {
            'id': {'type': 'string'},
            'description': {'type': 'string'},
            'status': {'type': 'string'},
            'url': {'type': 'string'},
            'last_status_change_by': {'type': 'string'},
            'created_at': {'type': 'string', 'format': 'date-time'},
            'last_updated_at': {'type': 'string', 'format': 'date-time'}
            },
        }

def discover(config):
    singer.write_schema('pagerduty', schema(), 'id')


def main():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    singer.write_schema('pagerduty', schema(), 'id')
    if args.discover:
        return
    incidents = get_pagerduty_incidents(args.config)
    singer.write_records('pagerduty', incidents)

if __name__ == "__main__":
    main()
