import React from 'react';
import PropTypes from 'prop-types';
import {Modal, Header, Button} from 'semantic-ui-react';

const AddWidgetDialog = ({ widgets, isModalOpen, onRequestClose, onWidgetSelect}) => {
  const widgetItems = Object.keys(widgets).map((widget, key) => {
    return (
      <div key={key} className="list-group">
        <a href="#" className="list-group-item" onClick={() => onWidgetSelect(widget)}>
          <h6 className="list-group-item-heading">{widgets[widget].title}</h6>
        </a>
      </div>
    );
  });
  
  return (
    <div style={styles.content}>
    <Modal
      open={isModalOpen}
      onClose={onRequestClose}
      closeIcon
      size='small'
    >
      <Modal.Header>
        Pick a widget to add
      </Modal.Header>
      <Modal.Content>
         {widgetItems}
      </Modal.Content>
      <Modal.Actions>
        <Button primary onClick={onRequestClose}>
          Close
        </Button>
      </Modal.Actions>
    </Modal>
    </div>
  );
};

AddWidgetDialog.propTypes = {
  widgets: PropTypes.object,
  isModalOpen: PropTypes.bool,
  onRequestClose: PropTypes.func,
  onWidgetSelect: PropTypes.func,
};

const styles = {
    content : {
        position              : 'absolute',
        top                   : '50%',
        left                  : '50%',
        right                 : 'auto',
        bottom                : 'auto',
        marginRight           : '-50%',
        transform             : 'translate(-50%, -50%)',
    },
    modal : {
      marginTop: '0px !important',
      marginLeft: 'auto',
      marginRight: 'auto'
  }
}

export default AddWidgetDialog;